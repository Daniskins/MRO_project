
(() => {
  const endpoint = "/api/planes";

  const form = document.getElementById("addAircraftForm");
  const submitBtn = form.querySelector('button[type="submit"]');

  function showMessage(text, type="info") {
    let node = document.getElementById("formMessage");
    if (!node) {
      node = document.createElement("div");
      node.id = "formMessage";
      form.parentNode.insertBefore(node, form);
    }
    node.textContent = text || "";
    node.style.display = text ? "block" : "none";
    node.style.color = type === "error" ? "#b00020" : "#155724";
    node.style.background = type === "error" ? "#f8d7da" : "#d4edda";
    node.style.padding = "8px";
    node.style.borderRadius = "4px";
    node.style.marginBottom = "10px";
  }

  function buildPayload(formEl) {
    const fd = new FormData(formEl);
    const raw = Object.fromEntries(fd.entries());

    // Маппинг под PlaneCreate
    return {
      type_plane: raw.aircraftType?.trim(),               // REQUIRED
      serial_number: raw.registration?.trim(),            // REQUIRED (заводской номер)
      tail_number: raw.modelVersion?.trim(),              // REQUIRED? (зависит от твоей схемы)
      base_airfield: raw.aerodrom_base?.trim(),           // REQUIRED
      belong_plane: raw.operator?.trim(),                 // REQUIRED
      operating_time: raw.initialHours ? Number(raw.initialHours) : 0, // REQUIRED (int)
      manufacturer_date: raw.entryDate || null            // date | null (YYYY-MM-DD)
    };
  }

  function validate(payload) {
    const required = ["type_plane", "serial_number", "base_airfield", "belong_plane", "operating_time"];
    for (const k of required) {
      if (payload[k] === null || payload[k] === undefined || String(payload[k]).trim() === "") {
        showMessage(`Поле "${k}" обязательно.`, "error");
        return false;
      }
    }

    if (Number.isNaN(payload.operating_time)) {
      showMessage('Поле "operating_time" должно быть числом.', "error");
      return false;
    }
    if (payload.operating_time < 0) {
      showMessage('Поле "operating_time" не может быть отрицательным.', "error");
      return false;
    }

    // Если tail_number обязателен в схеме — добавь проверку:
    if (!payload.tail_number || payload.tail_number.trim() === "") {
      showMessage('Поле "tail_number" (бортовой номер) обязательно.', "error");
      return false;
    }

    return true;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    showMessage("");

    const payload = buildPayload(form);
    if (!validate(payload)) return;

    submitBtn.disabled = true;
    const origText = submitBtn.textContent;
    submitBtn.textContent = "Отправка...";

    try {
      const resp = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(payload),
      });

      if (resp.ok) {
        const data = await resp.json().catch(() => null);
        showMessage("Борт успешно добавлен.", "success");

        // PlaneRead возвращает id
        if (data?.id != null) {
          // UI страница борта (не API)
          setTimeout(() => (window.location.href = `/planes/${data.id}`), 600);
        } else {
          form.reset();
        }
        return;
      }

      const err = await resp.json().catch(() => null);
      const detail = err?.detail;

      // Pydantic 422: detail=[{loc, msg, type}, ...]
      if (Array.isArray(detail)) {
        const msg = detail.map(d => `${(d.loc || []).join(".")}: ${d.msg}`).join("; ");
        showMessage(msg || `Ошибка сервера: ${resp.status}`, "error");
      } else {
        showMessage(detail || `Ошибка сервера: ${resp.status}`, "error");
      }
    } catch (err) {
      console.error(err);
      showMessage("Сетевая ошибка.", "error");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = origText;
    }
  });
})();
