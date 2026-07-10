/* ============================================================
   คอร์สปฏิบัติธรรม — Main Script
   render ทุกส่วนจากข้อมูลใน js/data.js
   ============================================================ */

/* ---------- ค่าคงที่สถานะคอร์ส ---------- */
const STATUS_LABEL = {
  open: "เปิดรับสมัคร",
  full: "เต็มแล้ว",
  closed: "ปิดรับสมัคร",
  soon: "เร็ว ๆ นี้",
};

const CATEGORY_LABEL = Object.fromEntries(
  CATEGORIES.map((c) => [c.id, c.title])
);

function badge(status) {
  return `<span class="badge badge-${status}">${STATUS_LABEL[status]}</span>`;
}

/* สร้าง markup รูปภาพ: ถ้าไฟล์รูปยังไม่ถูกวางใน images/
   จะซ่อน <img> แล้วโชว์กรอบ placeholder แทนโดยอัตโนมัติ */
function photoHTML(image, extraClass = "") {
  return `
  <figure class="photo ${extraClass}">
    <img src="${image.src}" alt="${image.alt || ""}"
      onerror="this.closest('.photo').classList.add('no-img')" />
    <span class="photo-fallback">
      <span class="placeholder-icon">🪷</span>
      <span class="placeholder-label">${image.alt || "รูปภาพ"}</span>
    </span>
  </figure>`;
}

/* ============================================================
   1) หมวดคอร์ส (Category Cards)
   ============================================================ */
function renderCategories() {
  const grid = document.getElementById("categoryGrid");
  grid.innerHTML = CATEGORIES.map(
    (cat) => `
    <div class="category-card" data-goto="${cat.id}">
      <span class="category-icon">${cat.icon}</span>
      <h3>${cat.title}</h3>
      <p>${cat.description}</p>
    </div>`
  ).join("");

  // คลิกการ์ดหมวด → เลื่อนไป section คอร์ส พร้อมเปิด filter หมวดนั้น
  grid.querySelectorAll(".category-card").forEach((card) => {
    card.addEventListener("click", () => {
      setFilter(card.dataset.goto);
      document.getElementById("courses").scrollIntoView({ behavior: "smooth" });
    });
  });
}

/* ============================================================
   2) คอร์สทั้งหมด + Filter Tabs
   ============================================================ */
function courseCard(course) {
  const canRegister = course.status === "open";
  const btn = canRegister
    ? `<a href="${course.registerUrl}" class="btn btn-primary btn-sm">สมัครคอร์สนี้</a>`
    : `<span class="btn btn-sm btn-disabled">${STATUS_LABEL[course.status]}</span>`;

  const image = CATEGORY_IMAGES[course.category];

  return `
  <article class="course-card" data-category="${course.category}">
    ${photoHTML(image, "course-card-img")}
    <div class="course-card-body">
      <div class="course-card-top">
        <h3>${course.title}</h3>
        ${badge(course.status)}
      </div>
      <p class="course-subtitle">${course.subtitle}</p>
      <div class="course-meta">
        <span><span class="meta-icon">📅</span>${course.dates}</span>
        <span><span class="meta-icon">⏳</span>${course.duration}</span>
        <span><span class="meta-icon">📍</span>${course.location}</span>
      </div>
      ${btn}
    </div>
  </article>`;
}

function renderCourses(filter) {
  const wrap = document.getElementById("courseList");
  const branchBlock = document.getElementById("branchBlock");

  const list = COURSES.filter((c) => c.category === filter);
  const subgroups = COURSE_SUBGROUPS[filter];

  if (subgroups) {
    // หมวดที่แยกกลุ่มย่อย เช่น 9 วัน / ออนไลน์ → คนใหม่, คนเก่า
    wrap.innerHTML = subgroups
      .map((group) => {
        const cards = list.filter((c) => c.subgroup === group.id);
        return `
        <div class="course-subgroup">
          <div class="subgroup-head">
            <h3 class="subgroup-title">${group.title}</h3>
            <p class="subgroup-note">${group.note}</p>
          </div>
          <div class="course-grid">${cards.map(courseCard).join("")}</div>
        </div>`;
      })
      .join("");
  } else {
    wrap.innerHTML = `<div class="course-grid">${list.map(courseCard).join("")}</div>`;
  }

  // แท็บ "สาขา" ไม่มี card — โชว์เฉพาะตารางสาขา
  branchBlock.style.display = filter === "branch" ? "block" : "none";
}

function setFilter(filter) {
  document.querySelectorAll("#filterTabs .tab").forEach((tab) => {
    const active = tab.dataset.filter === filter;
    tab.classList.toggle("active", active);
    tab.setAttribute("aria-selected", active);
  });
  renderCourses(filter);
}

function initTabs() {
  document.querySelectorAll("#filterTabs .tab").forEach((tab) => {
    tab.addEventListener("click", () => setFilter(tab.dataset.filter));
  });
}

/* ============================================================
   3) ตารางสาขา
   ============================================================ */
function renderBranches() {
  const tbody = document.getElementById("branchTableBody");
  tbody.innerHTML = BRANCHES.map((br) => {
    const link =
      br.status === "open"
        ? `<a href="${br.registerUrl}" class="table-link">สมัคร</a>`
        : `<span class="table-link table-link-disabled">—</span>`;
    return `
    <tr>
      <td class="course-name-cell">${br.name}</td>
      <td>${br.province}</td>
      <td>${br.courses}</td>
      <td>${badge(br.status)}</td>
      <td>${link}</td>
    </tr>`;
  }).join("");
}

/* ============================================================
   4) รูป Hero + แกลเลอรีบรรยากาศ
   ============================================================ */
function renderHeroPhoto() {
  const figure = document.getElementById("heroPhoto");
  const img = document.createElement("img");
  img.src = HERO_IMAGE.src;
  img.alt = HERO_IMAGE.alt;
  img.onerror = () => figure.classList.add("no-img");
  figure.prepend(img);
}

function renderGallery() {
  const grid = document.getElementById("galleryGrid");
  grid.innerHTML = GALLERY.map(
    (item) => `
    <div class="gallery-item">
      ${photoHTML({ src: item.src, alt: item.caption }, "gallery-photo")}
      <p class="gallery-caption">${item.caption}</p>
    </div>`
  ).join("");
}

/* ============================================================
   5) ขั้นตอนการสมัคร
   ============================================================ */
function renderSteps() {
  const grid = document.getElementById("stepsGrid");
  grid.innerHTML = STEPS.map(
    (step, i) => `
    <div class="step-card">
      <span class="step-number">${i + 1}</span>
      <h3>${step.title}</h3>
      <p>${step.description}</p>
    </div>`
  ).join("");
}

/* ============================================================
   6) FAQ Accordion
   ============================================================ */
function renderFaqs() {
  const list = document.getElementById("faqList");
  list.innerHTML = FAQS.map(
    (faq, i) => `
    <div class="faq-item">
      <button class="faq-question" aria-expanded="false" aria-controls="faq-answer-${i}">
        ${faq.q}
        <span class="faq-icon">＋</span>
      </button>
      <div class="faq-answer" id="faq-answer-${i}">
        <div class="faq-answer-inner">${faq.a}</div>
      </div>
    </div>`
  ).join("");

  list.querySelectorAll(".faq-item").forEach((item) => {
    const btn = item.querySelector(".faq-question");
    const answer = item.querySelector(".faq-answer");
    btn.addEventListener("click", () => {
      const isOpen = item.classList.toggle("open");
      btn.setAttribute("aria-expanded", isOpen);
      answer.style.maxHeight = isOpen ? answer.scrollHeight + "px" : "0";
    });
  });
}

/* ============================================================
   7) Footer — เติมข้อมูลติดต่อจาก SITE_INFO
   ============================================================ */
function renderFooter() {
  document.getElementById("footerSiteName").textContent = SITE_INFO.name;
  document.getElementById("footerAddress").textContent = SITE_INFO.address;
  document.getElementById("footerPhone").textContent = SITE_INFO.phone;
  document.getElementById("footerEmail").textContent = SITE_INFO.email;
  document.getElementById("footerLine").textContent = SITE_INFO.lineId;
  document.getElementById("footerFacebook").href = SITE_INFO.facebook;
}

/* ============================================================
   8) เมนูมือถือ
   ============================================================ */
function initMobileNav() {
  const toggle = document.getElementById("navToggle");
  const nav = document.getElementById("mainNav");

  toggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", isOpen);
  });

  // ปิดเมนูเมื่อคลิกลิงก์
  nav.querySelectorAll("a").forEach((a) =>
    a.addEventListener("click", () => {
      nav.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
    })
  );
}

/* ============================================================
   เริ่มต้น
   ============================================================ */
document.addEventListener("DOMContentLoaded", () => {
  renderHeroPhoto();
  renderCategories();
  renderCourses("nine-day");
  renderBranches();
  renderGallery();
  renderSteps();
  renderFaqs();
  renderFooter();
  initTabs();
  initMobileNav();
});
