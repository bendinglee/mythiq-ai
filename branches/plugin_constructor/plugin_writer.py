import os

def write_plugin_file(name, code):
    folder = "compiled_plugins"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{name}.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    return path
