def explain_error(error_msg):
    glossary = {
        "KeyError": "🧩 A value wasn't found. Check your data keys.",
        "ValueError": "⚠️ The format looks wrong — maybe numbers vs text?",
        "ImportError": "🚫 Could not load a file or library. Check your paths.",
        "TypeError": "📏 You're passing the wrong type — check strings vs numbers."
    }
    for key in glossary:
        if key in error_msg:
            return glossary[key]
    return "❔ Unknown error. Try simplifying your code or inputs."
