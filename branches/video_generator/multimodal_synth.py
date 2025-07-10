def synthesize_scene(prompt, image, audio):
    return {
        "scene": f"Video clip of '{prompt}' with visuals from '{image}' and audio '{audio}'",
        "status": "synthesized"
    }
