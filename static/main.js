document.getElementById("send-btn").onclick = async () => {
  const inputEl = document.getElementById("user-input");
  const logEl = document.getElementById("chat-log");
  const message = inputEl.value.trim();

  if (!message) return;

  logEl.innerHTML += `<div class="message user">🧑 ${message}</div>`;
  inputEl.value = "";

  const mode = document.querySelector(".nav-btn.active")?.dataset.mode || "chat";
  let endpoint = "/api/dispatch";

  if (mode === "math") endpoint = "/api/solve-math";
  if (mode === "image") endpoint = "/api/generate-image";
  if (mode === "reflect") endpoint = "/api/reflect-logs";

  const res = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: message, prompt: message })
  });

  const data = await res.json();
  const reply = data.result || data.message || data.output || "⚠️ No response";

  logEl.innerHTML += `<div class="message ai">🤖 ${reply}</div>`;
  logEl.scrollTop = logEl.scrollHeight;
};

document.querySelectorAll(".nav-btn").forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
  };
});
