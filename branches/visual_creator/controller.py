from branches.visual_creator.prompt_parser import parse_prompt
from branches.visual_creator.template_loader import load_template
from branches.visual_creator.style_engine import apply_style
from branches.visual_creator.image_synthesizer import synthesize_image
from branches.visual_creator.caption_overlay import add_overlay
from branches.visual_creator.visual_exporter import export_visual
from branches.visual_creator.visual_validator import validate_visual_request

def create_visual_asset(prompt, style="default", overlay=""):
    is_valid, msg = validate_visual_request(prompt, style)
    if not is_valid:
        return { "success": False, "error": msg }

    parsed = parse_prompt(prompt)
    template = load_template(style)
    styled = apply_style(parsed, template)
    image = synthesize_image(styled)
    if overlay:
        image = add_overlay(image, overlay)
    path = export_visual(image)
    return {
        "success": True,
        "image_url": path,
        "style": style,
        "overlay": overlay
    }
