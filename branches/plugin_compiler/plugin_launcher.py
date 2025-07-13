def run_plugin(name):
    try:
        module = __import__(f"compiled_plugins.{name}")
        return module.run("Hello")
    except Exception as e:
        return f"❌ Failed: {e}"
