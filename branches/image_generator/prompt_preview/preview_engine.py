from branches.image_generator.prompt_crafter import stylize_prompt

def generate_prompt_preview(prompt, style="cinematic"):
    styled = stylize_prompt(prompt, style)
    tag = f"[{style.lower()}]"

    # Extract modifier string for UI hint
    modifiers = styled.replace(tag, "").strip()

    return {
        "base_prompt": prompt.strip(),
        "style": style,
        "final_prompt": styled,
        "modifier_hint": modifiers
    }
