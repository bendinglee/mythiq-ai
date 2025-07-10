def apply_style(prompt, template):
    filters = template.get("filters", [])
    styled = prompt
    for f in filters:
        styled += f" + {f}"
    return styled
