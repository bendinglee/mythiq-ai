document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("math-form");
  const input = document.getElementById("math-question");
  const outputBox = document.getElementById("math-output");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const question = input.value.trim();

    if (!question) {
      outputBox.textContent = "⚠️ Please enter a math question.";
      return;
    }

    outputBox.textContent = "🧠 Solving...";

    try {
      const res = await fetch("/api/solve-math", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      });

      const data = await res.json();

      if (data.success) {
        outputBox.textContent = `✅ Result: ${data.result}`;
      } else {
        outputBox.textContent = `⚠️ Error: ${data.error || "Unknown failure"}`;
      }
    } catch (err) {
      outputBox.textContent = `❌ Request error: ${err.message}`;
    }
  });
});
