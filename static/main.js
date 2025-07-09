// 🚀 Handle Send Button
document.getElementById("send-btn").onclick = async () => {
  const inputEl = document.getElementById("user-input");
  const logEl = document.getElementById("chat-log");
  const message = inputEl.value.trim();

  if (!message) return;

  // 💬 Log user input
  logEl.innerHTML += `<div class="message user">🧑 ${message}</div>`;
  inputEl.value = "";

  // 🧭 Detect active mode from sidebar
  const mode = document.querySelector(".nav-btn.active")?.dataset.mode || "chat";
  let endpoint = "/api/dispatch";

  if (mode === "math") endpoint = "/api/solve-math";
  if (mode === "image") endpoint = "/api/generate-image";
  if (mode === "reflect") endpoint = "/api/reflect-logs";

  try {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: message, prompt: message })
    });

    const data = await res.json();
    const reply = data.result || data.message || data.output || "⚠️ No response";

    // 🤖 Log AI response
    logEl.innerHTML += `<div class="message ai">🤖 ${reply}</div>`;
    logEl.scrollTop = logEl.scrollHeight;

    // 🧠 Refresh memory sidebar after response
    loadMemorySnapshot();
  } catch (error) {
    logEl.innerHTML += `<div class="message ai">⚠️ Error: ${error.message}</div>`;
  }
};

// 🔁 Sidebar Mode Switching
document.querySelectorAll(".nav-btn").forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
  };
});

// 🧠 Load Recent Memory Entries
async function loadMemorySnapshot() {
  try {
    const res = await fetch("/api/recall");
    const data = await res.json();
    const list = document.getElementById("memory-list");
    list.innerHTML = "";

    const logs = data.logs || [];
    logs.slice(-5).reverse().forEach(entry => {
      const li = document.createElement("li");
      li.textContent = entry.input || entry.output || "[Empty log]";
      list.appendChild(li);
    });
  } catch (err) {
    document.getElementById("memory-list").innerHTML = "<li>⚠️ Error loading memory</li>";
  }
}

loadMemorySnapshot();
