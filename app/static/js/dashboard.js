  // ====== Минимальный JS: заглушки + точка расширения под ваши API ======
// Если у тебя эндпоинт другой (например /api/uavs/), поменяй тут:
const API_UAVS = "/api/uavs";

// Заглушки для задач (потом заменишь на /api/maintenance-records, /api/maintenance-types и т.д.)
const mockTasks = [
  { title: "Проверить сроки ТО по парку БПЛА", meta: "3 аппарата требуют внимания", priority: "warn", link: "/reports" },
  { title: "БПЛА близки к порогу наработки для ТО-1", meta: "2 аппарата в зоне риска", priority: "warn", link: "/maintenance-records" },
  { title: "Журнал наработки: новые вылеты без подтверждения", meta: "1 запись на ревью", priority: "ok", link: "/operating-time-logs" },
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
    // Подстрой имена полей под твою схему UavRead.
    const model = p.uav_model ?? p.model ?? "—";
    const tail = p.tail_number ?? p.registration ?? p.board_number ?? "—";
    const msn  = p.serial_number ?? p.msn ?? "—";
    const fh   = p.total_operating_time ?? p.flight_hours ?? p.hours ?? "—";
    const st   = (p.status ?? "active").toString();

    let dot = "ok";
    if (st.toLowerCase().includes("decommission") || st.toLowerCase().includes("critical")) dot = "bad";
    if (st.toLowerCase().includes("maintenance") || st.toLowerCase().includes("due")) dot = "warn";

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${model}</td>
      <td><strong>${tail}</strong></td>
      <td>${msn}</td>
      <td>${fh}</td>
      <td><span class="status"><span class="dot ${dot}"></span>${st}</span></td>
      <td><a class="link" href="/uavs/${p.id ?? ""}">Открыть</a></td>
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
        p.uav_model, p.model, p.tail_number, p.registration, p.board_number, p.serial_number, p.msn
      ].filter(Boolean).map(v => String(v).toLowerCase());
      return values.some(v => v.includes(q));
    });
    renderFleetRows(filtered);
  });
}

async function loadFleet() {
  try {
    const resp = await fetch(API_UAVS);
    if (!resp.ok) throw new Error("HTTP " + resp.status);
    const uavs = await resp.json();

    setKpi("kpi-fleet", Array.isArray(uavs) ? uavs.length : "—");

    // Остальные KPI пока заглушки
    setKpi("kpi-aog", "0");
    setKpi("kpi-overdue", "0");
    setKpi("kpi-lowstock", "0");

    const list = Array.isArray(uavs) ? uavs : [];
    renderFleetRows(list);
    setupFleetSearch(list);
  } catch (e) {
    const demo = [
      { id: 1, uav_model: "Орлан-10", tail_number: "КН-07", serial_number: "95101", total_operating_time: 245, status: "active" },
      { id: 2, uav_model: "ZALA 421-16E", tail_number: "902", serial_number: "49083507902", total_operating_time: 512, status: "in_maintenance" },
      { id: 3, uav_model: "Суперкам S350", tail_number: "35", serial_number: "9009005535", total_operating_time: 50, status: "active" },
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
