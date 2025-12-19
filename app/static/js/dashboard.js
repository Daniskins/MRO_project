  // ====== Минимальный JS: заглушки + точка расширения под ваши API ======
// Если у тебя эндпоинт другой (например /api/planes/), поменяй тут:
const API_PLANES = "/api/planes";

// Заглушки для задач (потом заменишь на /api/work-orders, /api/inspections и т.д.)
const mockTasks = [
  { title: "Проверить сроки инспекций по флоту", meta: "3 позиции требуют внимания", priority: "warn", link: "/reports" },
  { title: "Склад: минимальные остатки по критическим деталям", meta: "2 позиции low stock", priority: "warn", link: "/inventory" },
  { title: "Work Orders: ожидают подтверждения", meta: "1 заказ на ревью", priority: "ok", link: "/work-orders" },
];

function formatNow() {
  const d = new Date();
  return d.toLocaleString("ru-RU", { year:"numeric", month:"2-digit", day:"2-digit", hour:"2-digit", minute:"2-digit" });
}

function setKpi(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function renderTasks(tasks) {
  const ul = document.getElementById("tasks-list");
  ul.innerHTML = "";
  tasks.forEach(t => {
    const li = document.createElement("li");
    li.className = "item";
    li.innerHTML = `
      <div>
        <div class="title">${t.title}</div>
        <div class="meta">${t.meta}</div>
      </div>
      <div class="right">
        <span class="status"><span class="dot ${t.priority}"></span>${t.priority.toUpperCase()}</span>
        <a class="link" href="${t.link}">Открыть</a>
      </div>
    `;
    ul.appendChild(li);
  });
}

function renderFleetRows(items) {
  const tbody = document.getElementById("fleet-tbody");
  tbody.innerHTML = "";

  items.slice(0, 12).forEach(p => {
    // Подстрой имена полей под твою схему PlaneRead.
    const model = p.model ?? p.aircraft_type ?? "—";
    const tail = p.tail_number ?? p.registration ?? p.board_number ?? "—";
    const msn  = p.serial_number ?? p.msn ?? "—";
    const fh   = p.flight_hours ?? p.fh ?? p.hours ?? "—";
    const st   = (p.status ?? "OK").toString();

    let dot = "ok";
    if (st.toLowerCase().includes("aog") || st.toLowerCase().includes("critical")) dot = "bad";
    if (st.toLowerCase().includes("due") || st.toLowerCase().includes("warn")) dot = "warn";

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${model}</td>
      <td><strong>${tail}</strong></td>
      <td>${msn}</td>
      <td>${fh}</td>
      <td><span class="status"><span class="dot ${dot}"></span>${st}</span></td>
      <td><a class="link" href="/planes/${p.id ?? ""}">Открыть</a></td>
    `;
    tbody.appendChild(tr);
  });
}

function setupFleetSearch(all) {
  const input = document.getElementById("fleet-search");
  input.addEventListener("input", () => {
    const q = input.value.trim().toLowerCase();
    if (!q) return renderFleetRows(all);

    const filtered = all.filter(p => {
      const values = [
        p.model, p.aircraft_type, p.tail_number, p.registration, p.board_number, p.serial_number, p.msn
      ].filter(Boolean).map(v => String(v).toLowerCase());
      return values.some(v => v.includes(q));
    });
    renderFleetRows(filtered);
  });
}

async function loadFleet() {
  try {
    const resp = await fetch(API_PLANES);
    if (!resp.ok) throw new Error("HTTP " + resp.status);
    const planes = await resp.json();

    setKpi("kpi-fleet", Array.isArray(planes) ? planes.length : "—");

    // Остальные KPI пока заглушки
    setKpi("kpi-aog", "0");
    setKpi("kpi-overdue", "0");
    setKpi("kpi-lowstock", "0");

    const list = Array.isArray(planes) ? planes : [];
    renderFleetRows(list);
    setupFleetSearch(list);
  } catch (e) {
    const demo = [
      { id: 1, model: "Sukhoi Superjet 100", tail_number: "RA-89001", serial_number: "95101", flight_hours: 12450, status: "OK" },
      { id: 2, model: "Су-35", tail_number: "902", serial_number: "49083507902", flight_hours: 12500, status: "DUE" },
      { id: 3, model: "Су-57", tail_number: "35", serial_number: "9009005535", flight_hours: 5000, status: "AOG" },
    ];
    setKpi("kpi-fleet", demo.length);
    setKpi("kpi-aog", "1");
    setKpi("kpi-overdue", "1");
    setKpi("kpi-lowstock", "2");
    renderFleetRows(demo);
    setupFleetSearch(demo);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("year").textContent = new Date().getFullYear();
  document.getElementById("last-updated").textContent = "Обновлено: " + formatNow();
  renderTasks(mockTasks);
  loadFleet();
});
