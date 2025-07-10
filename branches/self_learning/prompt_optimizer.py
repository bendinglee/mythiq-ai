def optimize_prompt(prompt):
    fixes = []
    prompt = prompt.strip()

    if len(prompt.split()) < 5:
        prompt += " please provide more details"
        fixes.append("📝 Extended short prompt.")

    if "I don't know" in prompt:
        prompt = prompt.replace("I don't know", "I'm curious about")
        fixes.append("🔄 Rephrased vague language.")

    return { "optimized": prompt, "fixes": fixes }
