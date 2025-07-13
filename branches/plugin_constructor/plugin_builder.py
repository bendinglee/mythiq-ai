def build_plugin_code(config):
    name = config.get("name", "my_plugin")
    func = config.get("function_name", "run")
    desc = config.get("description", "Generated plugin")
    logic = config.get("logic", 'return "Hello from plugin!"')

    return f'''
# Plugin: {name}
# Description: {desc}

def {func}(input):
    {logic}
'''
