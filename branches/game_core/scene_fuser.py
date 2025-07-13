def fuse_scene(prompt, style="cyberpunk"):
    elements = [f"{style} rendering", "dynamic lighting", "emotive soundtrack"]
    return { "prompt": prompt, "style": style, "scene_elements": elements }
