document.getElementById("reflect-btn").onclick = async () => {
  const res = await fetch("/api/reflect-logs", { method: "POST" });
  const data = await res.json();
  document.getElementById("reflect-output").innerText = JSON.stringify(data, null, 2);
};

document.getElementById("solve-btn").onclick = async () => {
  const q = document.getElementById("math-q").value;
  const res = await fetch("/api/solve-math", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ question: q })
  });
  const data = await res.json();
  document.getElementById("math-output").innerText = data.result || data.error;
};

document.getElementById("gen-img-btn").onclick = async () => {
  const prompt = document.getElementById("image-prompt").value;
  const res = await fetch("/api/generate-image", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ prompt })
  });
  const data = await res.json();
  const imageEl = document.createElement("img");
  imageEl.src = data.image_url || "";
  imageEl.style = "max-width:100%;border-radius:8px;";
  const resultDiv = document.getElementById("image-result");
  resultDiv.innerHTML = ""; resultDiv.appendChild(imageEl);
};
