import zipfile, json

def export_plugin(name, code):
    with zipfile.ZipFile(f"{name}_plugin.zip", "w") as z:
        z.writestr(f"{name}.py", code)
    with open(f"{name}.json", "w") as j:
        json.dump({ "name": name, "code": code }, j)
    return { "zip": f"{name}_plugin.zip", "json": f"{name}.json" }
