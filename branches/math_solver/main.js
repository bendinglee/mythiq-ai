document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("math-form");
  const input = document.getElementById("math-question");
  const outputBox = document.getElementById("math-output");
  const historyList = document.getElementById("math-history");

  const renderResult = (data) => {
    if (data.success) {
      const solution = data.solution || data.result;
      const confidence = data.confidence || 0.9;

      outputBox.innerHTML = `
        ✅ <strong>Solution:</strong> ${solution}<br/>
        📊 <strong>Confidence:</strong> ${Math.round(confidence * 100)}%
      `;

      addToHistory(input.value.trim(), solution);
    } else {
      outputBox.innerHTML = `⚠️ <strong>Error:</strong> ${data.error || "Unknown failure"}`;
    }
  };

  const addToHistory = (query, result) => {
    if (!historyList) return;
    const li = document.createElement("li");
    li.innerHTML = `<code>${query}</code> → ${result}`;
    historyList.prepend(li);
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const question = input.value.trim();

    if (!question) {
      outputBox.textContent = "⚠️ Please enter a math question.";
      return;
    }

    outputBox.textContent = "🧠 Solving...";
    form.classList.add("solving");

    try {
      const res = await fetch("/api/solve-math", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      });

      const data = await res.json();
      renderResult(data);
    } catch (err) {
      outputBox.textContent = `❌ Request error: ${err.message}`;
    } finally {
      form.classList.remove("solving");
    }
  });
});
