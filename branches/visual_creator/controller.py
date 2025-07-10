from branches.visual_creator.prompt_parser import parse_prompt
from branches.visual_creator.style_engine import apply_style
from branches.visual_creator.image_synthesizer import synthesize_image
from branches.visual_creator.caption_overlay import add_overlay
from branches.visual_creator.visual_exporter import export_visual

def create_visual_asset(prompt, style="default", overlay=""):
    parsed = parse_prompt(prompt)
    styled = apply_style(parsed, style)
    image = synthesize_image(styled)
    if overlay:
        image = add_overlay(image, overlay)
    path = export_visual(image)
    return { "success": True, "image_url": path }
