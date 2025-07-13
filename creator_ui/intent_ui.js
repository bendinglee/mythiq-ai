async function submit() {
  const data = {
    preset: document.getElementById("preset").value,
    tone: document.getElementById("tone").value,
    plugin_overrides: document.getElementById("plugins").value.split(",")
  };
  const res = await fetch("/api/intent-ui", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  const json = await res.json();
  document.getElementById("output").innerText = JSON.stringify(json.updated, null, 2);
}
