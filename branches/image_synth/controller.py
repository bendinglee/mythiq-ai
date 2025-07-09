from branches.image_synth.engine import synthesize_image
from branches.image_synth.memory_writer import log_synth_output

def process_image_synthesis(prompt, modifiers=None):
    # 🖼️ Run synthesis via engine (e.g. upscaling, filtering)
    result = synthesize_image(prompt, modifiers)

    # 🧠 Log result to memory
    log_synth_output(prompt, result, modifiers)

    # ✅ Return standardized response object
    return {
        "success": result.get("success", False),
        "prompt": prompt,
        "synth_url": result.get("synth_url", ""),
        "style_applied": result.get("style_applied", "default"),
        "message": "Image synthesis complete." if result.get("success") else "Image synthesis failed."
    }
