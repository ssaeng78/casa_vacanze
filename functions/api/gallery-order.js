const REPO = "ssaeng78/casa_vacanze";
const PATH = "images/gallery/manifest.json";
const BRANCH = "main";
const UA = "casa-vacanze-gallery";

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

const fetchManifestMeta = async (token) => {
  const res = await fetch(
    `https://api.github.com/repos/${REPO}/contents/${PATH}?ref=${BRANCH}`,
    { headers: ghHeaders(token) }
  );
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`github_read_${res.status}:${text.slice(0, 200)}`);
  }
  return res.json();
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

const normalizeImages = (images) => {
  if (!Array.isArray(images)) return null;
  const cleaned = images
    .map((item) => String(item || "").trim().replace(/^\.\//, ""))
    .filter(Boolean)
    .map((file) => (file.startsWith("images/") ? file : `images/gallery/${file.replace(/^.*[/\\]/, "")}`));
  return cleaned.length ? cleaned : null;
};

export async function onRequestGet(context) {
  try {
    const token = context.env.GITHUB_TOKEN || "";
    const meta = await fetchManifestMeta(token);
    const parsed = JSON.parse(decodeContent(meta.content));
    const images = normalizeImages(parsed.images);
    if (!images) return json({ error: "invalid_manifest" }, 502);
    return json({ images, sha: meta.sha, source: "github" });
  } catch (err) {
    return json({ error: "read_failed", detail: String(err.message || err) }, 502);
  }
}

export async function onRequestPost(context) {
  const token = context.env.GITHUB_TOKEN;
  if (!token) {
    return json(
      {
        error: "missing_token",
        message: "ตั้งค่า GITHUB_TOKEN ใน Cloudflare Pages ก่อน (ครั้งเดียว)",
      },
      503
    );
  }

  const saveKey = context.env.GALLERY_SAVE_KEY;
  if (saveKey) {
    const provided = context.request.headers.get("X-Gallery-Key") || "";
    if (provided !== saveKey) {
      return json({ error: "unauthorized" }, 401);
    }
  }

  let body;
  try {
    body = await context.request.json();
  } catch {
    return json({ error: "invalid_json" }, 400);
  }

  const images = normalizeImages(body && body.images);
  if (!images) return json({ error: "images_required" }, 400);

  try {
    const meta = await fetchManifestMeta(token);
    const payload = `${JSON.stringify({ images }, null, 2)}\n`;
    const res = await fetch(`https://api.github.com/repos/${REPO}/contents/${PATH}`, {
      method: "PUT",
      headers: {
        ...ghHeaders(token),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: "chore(gallery): update photo order",
        content: encodeContent(payload),
        sha: meta.sha,
        branch: BRANCH,
      }),
    });

    if (!res.ok) {
      const text = await res.text();
      return json({ error: "write_failed", detail: text.slice(0, 300) }, 502);
    }

    const result = await res.json();
    return json({
      ok: true,
      images,
      sha: result.content && result.content.sha,
      commit: result.commit && result.commit.sha,
    });
  } catch (err) {
    return json({ error: "write_failed", detail: String(err.message || err) }, 502);
  }
}
