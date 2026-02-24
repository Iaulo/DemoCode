const $ = (sel) => document.querySelector(sel);

const state = {
  theme: localStorage.getItem("theme") || "light",
};

function setTheme(theme) {
  state.theme = theme;
  document.documentElement.dataset.theme = theme;
  localStorage.setItem("theme", theme);
}

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || `HTTP ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

function renderItems(items) {
  const list = $("#itemsList");
  list.innerHTML = "";
  $("#empty").style.display = items.length ? "none" : "block";

  for (const it of items) {
    const li = document.createElement("li");
    li.className = "item";
    li.dataset.id = it.id;

    const left = document.createElement("div");
    left.className = "left";

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = it.done;
    cb.ariaLabel = `Marcar ${it.title}`;
    cb.addEventListener("change", async () => {
      await api(`/api/items/${it.id}/toggle`, { method: "POST" });
      await loadItems();
    });

    const span = document.createElement("span");
    span.textContent = it.title;
    span.className = it.done ? "done" : "";

    left.appendChild(cb);
    left.appendChild(span);

    const del = document.createElement("button");
    del.textContent = "🗑️";
    del.ariaLabel = `Borrar ${it.title}`;
    del.addEventListener("click", async () => {
      await api(`/api/items/${it.id}`, { method: "DELETE" });
      await loadItems();
    });

    li.appendChild(left);
    li.appendChild(del);
    list.appendChild(li);
  }
}

async function loadItems() {
  $("#error").textContent = "";
  const q = $("#searchInput").value.trim();
  const data = await api(`/api/items${q ? `?q=${encodeURIComponent(q)}` : ""}`);
  renderItems(data.items);
}

function wireEvents() {
  $("#createForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    $("#error").textContent = "";
    const title = $("#titleInput").value;
    try {
      await api("/api/items", { method: "POST", body: JSON.stringify({ title }) });
      $("#titleInput").value = "";
      await loadItems();
    } catch (err) {
      $("#error").textContent = err.message;
    }
  });

  $("#refreshBtn").addEventListener("click", loadItems);

  $("#searchInput").addEventListener("input", () => {
    // debounce simple
    clearTimeout(window.__t);
    window.__t = setTimeout(loadItems, 200);
  });

  $("#themeBtn").addEventListener("click", () => {
    setTheme(state.theme === "light" ? "dark" : "light");
  });

  $("#buildInfo").textContent = `Build: sin bundler (vanilla).`;
}

setTheme(state.theme);
wireEvents();
loadItems();
