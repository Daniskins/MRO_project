
(() => {
  const endpoint = "/api/uavs";

  const form = document.getElementById("addUavForm");
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

    // Маппинг под UavCreate
    return {
      uav_model: raw.uavModel?.trim(),                       // REQUIRED
      serial_number: raw.serialNumber?.trim(),                // REQUIRED
      tail_number: raw.tailNumber?.trim(),                    // REQUIRED (есть значение по умолчанию)
      base_location: raw.baseLocation?.trim(),                // REQUIRED
      operator: raw.operator?.trim(),                         // REQUIRED
      status: raw.status || "active",
      total_operating_time: raw.initialHours ? Number(raw.initialHours) : 0, // REQUIRED (int)
      manufacture_date: raw.manufactureDate || null           // date | null (YYYY-MM-DD)
    };
  }

  function validate(payload) {
    const required = ["uav_model", "serial_number", "base_location", "operator"];
    for (const k of required) {
      if (payload[k] === null || payload[k] === undefined || String(payload[k]).trim() === "") {
        showMessage(`Поле "${k}" обязательно.`, "error");
        return false;
      }
    }

    if (Number.isNaN(payload.total_operating_time)) {
      showMessage('Поле "total_operating_time" должно быть числом.', "error");
      return false;
    }
    if (payload.total_operating_time < 0) {
      showMessage('Поле "total_operating_time" не может быть отрицательным.', "error");
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
        showMessage("БПЛА успешно добавлен.", "success");

        // UavRead возвращает id
        if (data?.id != null) {
          setTimeout(() => (window.location.href = `/uavs/${data.id}`), 600);
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
