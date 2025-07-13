import zipfile, json

def export_plugin_bundle(name, code):
    zip_path = f"{name}_plugin.zip"
    json_path = f"{name}.plugin.json"

    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.writestr(f"{name}.py", code)

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump({ "name": name, "code": code }, jf, indent=2)

    return { "zip": zip_path, "json": json_path }
