const REPO = "ssaeng78/casa_vacanze";
const PATH = "images/gallery/manifest.json";
const BRANCH = "main";
const UA = "casa-vacanze-gallery";
const WORKER_URL = "https://casa-gallery-order.fancy-angelfish.workers.dev/";

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
    },
  });

const ghHeaders = (token) => {
  const headers = {
    Accept: "application/vnd.github+json",
    "User-Agent": UA,
    "X-GitHub-Api-Version": "2022-11-28",
  };
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
};

const normalizeImages = (images) => {
  if (!Array.isArray(images)) return null;
  const cleaned = images
    .map((item) => String(item || "").trim().replace(/^\.\//, ""))
    .filter(Boolean)
    .map((file) =>
      file.startsWith("images/") ? file : `images/gallery/${file.replace(/^.*[/\\]/, "")}`
    );
  return cleaned.length ? cleaned : null;
};

const decodeContent = (content) => {
  const normalized = String(content || "").replace(/\n/g, "");
  const binary = atob(normalized);
  const bytes = Uint8Array.from(binary, (c) => c.charCodeAt(0));
  return new TextDecoder().decode(bytes);
};

const encodeContent = (text) => {
  const bytes = new TextEncoder().encode(text);
  let binary = "";
  bytes.forEach((b) => {
    binary += String.fromCharCode(b);
  });
  return btoa(binary);
};

async function readFromWorker() {
  const res = await fetch(WORKER_URL, {
    headers: { Accept: "application/json", "User-Agent": UA },
  });
  if (!res.ok) return null;
  const ct = res.headers.get("content-type") || "";
  if (!ct.includes("application/json")) return null;
  const data = await res.json();
  return normalizeImages(data.images);
}

async function writeToWorker(images) {
  const res = await fetch(WORKER_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      "User-Agent": UA,
    },
    body: JSON.stringify({ images }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`worker_${res.status}:${text.slice(0, 120)}`);
  }
  const ct = res.headers.get("content-type") || "";
  if (!ct.includes("application/json")) throw new Error("worker_non_json");
  const data = await res.json();
  if (!data.ok) throw new Error(data.error || "worker_failed");
  return data;
}

async function readFromGithub(token) {
  const res = await fetch(
    `https://api.github.com/repos/${REPO}/contents/${PATH}?ref=${BRANCH}`,
    { headers: ghHeaders(token) }
  );
  if (!res.ok) throw new Error(`github_read_${res.status}`);
  const meta = await res.json();
  const parsed = JSON.parse(decodeContent(meta.content));
  return { images: normalizeImages(parsed.images), sha: meta.sha };
}

async function writeToGithub(token, images, sha) {
  const payload = `${JSON.stringify({ images }, null, 2)}\n`;
  const res = await fetch(`https://api.github.com/repos/${REPO}/contents/${PATH}`, {
    method: "PUT",
    headers: { ...ghHeaders(token), "Content-Type": "application/json" },
    body: JSON.stringify({
      message: "chore(gallery): update photo order",
      content: encodeContent(payload),
      sha,
      branch: BRANCH,
    }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`github_write_${res.status}:${text.slice(0, 160)}`);
  }
  return res.json();
}

async function readFromKvEnv(env) {
  const account = env.CF_ACCOUNT_ID;
  const ns = env.CF_KV_NAMESPACE_ID;
  const token = env.CF_API_TOKEN;
  if (!account || !ns || !token) return null;
  const url = `https://api.cloudflare.com/client/v4/accounts/${account}/storage/kv/namespaces/${ns}/values/order`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${token}`, "User-Agent": UA },
  });
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`kv_read_${res.status}`);
  return normalizeImages(await res.json());
}

async function writeToKvEnv(env, images) {
  const account = env.CF_ACCOUNT_ID;
  const ns = env.CF_KV_NAMESPACE_ID;
  const token = env.CF_API_TOKEN;
  if (!account || !ns || !token) return false;
  const url = `https://api.cloudflare.com/client/v4/accounts/${account}/storage/kv/namespaces/${ns}/values/order`;
  const res = await fetch(url, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "text/plain",
      "User-Agent": UA,
    },
    body: JSON.stringify(images),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`kv_write_${res.status}:${text.slice(0, 160)}`);
  }
  return true;
}

export async function onRequestGet(context) {
  try {
    try {
      const images = await readFromKvEnv(context.env);
      if (images) return json({ images, source: "kv" });
    } catch (_) {
      /* fall through */
    }

    try {
      const images = await readFromWorker();
      if (images) return json({ images, source: "worker" });
    } catch (_) {
      /* fall through */
    }

    const token = context.env.GITHUB_TOKEN || "";
    const { images } = await readFromGithub(token);
    if (!images) return json({ error: "invalid_manifest" }, 502);
    return json({ images, source: "github" });
  } catch (err) {
    return json({ error: "read_failed", detail: String(err.message || err) }, 502);
  }
}

export async function onRequestPost(context) {
  let body;
  try {
    body = await context.request.json();
  } catch {
    return json({ error: "invalid_json" }, 400);
  }

  const images = normalizeImages(body && body.images);
  if (!images) return json({ error: "images_required" }, 400);

  const saveKey = context.env.GALLERY_SAVE_KEY;
  if (saveKey) {
    const provided = context.request.headers.get("X-Gallery-Key") || "";
    if (provided !== saveKey) return json({ error: "unauthorized" }, 401);
  }

  // 1) KV via Cloudflare env vars (if configured on Pages)
  try {
    if (await writeToKvEnv(context.env, images)) {
      return json({ ok: true, images, via: "kv" });
    }
  } catch (_) {
    /* fall through */
  }

  // 2) Dedicated order worker
  try {
    await writeToWorker(images);
    return json({ ok: true, images, via: "worker" });
  } catch (workerErr) {
    // 3) Optional GitHub token on Pages
    const token = context.env.GITHUB_TOKEN;
    if (!token) {
      return json(
        {
          error: "store_failed",
          message: "บันทึกไม่สำเร็จ",
          detail: String(workerErr.message || workerErr),
        },
        503
      );
    }
    try {
      const meta = await readFromGithub(token);
      await writeToGithub(token, images, meta.sha);
      return json({ ok: true, images, via: "github" });
    } catch (err) {
      return json({ error: "write_failed", detail: String(err.message || err) }, 502);
    }
  }
}
