from branches.tutorial_mode.faq_loader import load_faq
from branches.tutorial_mode.preset_bank_loader import load_presets

def render_tutorial():
    faq = load_faq()
    presets = load_presets()

    return {
        "success": True,
        "title": "🧠 Mythiq Beginner Guide",
        "faq": faq,
        "presets": presets,
        "tips": [
            "Use clear prompts like 'summarize this paragraph'.",
            "Try tone styles: friendly, formal, curious.",
            "Explore plugin mode for creative tools."
        ]
    }
