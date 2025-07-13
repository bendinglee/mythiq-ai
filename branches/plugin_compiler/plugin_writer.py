import os

def write_plugin(name, code):
    path = f"compiled_plugins/{name}.py"
    os.makedirs("compiled_plugins", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    return path
