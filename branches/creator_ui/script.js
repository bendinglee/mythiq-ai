async function runCreator() {
  const prompt = document.getElementById("promptInput").value;
  const mode = document.getElementById("modeSelect").value;
  const style = document.getElementById("styleSelect").value;

  const response = await fetch("/creator-mode", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, mode, style })
  });

  const result = await response.json();
  const preview = document.getElementById("outputPreview");

  if (!result.success) {
    preview.innerHTML = `<p>❌ Error: ${result.error}</p>`;
  } else if (result.image_url) {
    preview.innerHTML = `<img src="${result.image_url}" alt="Generated image" />`;
  } else if (result.video_url) {
    preview.innerHTML = `<video controls src="${result.video_url}"></video>`;
  } else {
    preview.innerHTML = `<p>✅ Output received.</p>`;
  }
}
