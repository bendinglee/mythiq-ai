import re

def simplify_prompt(text):
    if not isinstance(text, str) or len(text.strip()) < 5:
        return "🧠 Prompt too short or missing."

    replacements = {
        r"\bIn essence[,|:]*": "",  # Remove lead-in fluff
        r"\bHerein lies\b": "Here is",
        r"\bIt can be observed that\b": "We see that",
        r"\bIt is known that\b": "We know that",
        r"\bThe following exposition reveals\b": "Here’s what’s happening",
        r"\bThe aforementioned\b": "Earlier",
        r"\bOne may infer that\b": "It suggests",
        r"\bTherefore[,|:]*": "So",
        r"\bConsequently[,|:]*": "That means",
        r"\bHence[,|:]*": "So",
        r"\bThus[,|:]*": "So",
        r"\bWhereas\b": "But",
        r"\bPrior to\b": "Before",
        r"\bSubsequent to\b": "After",
        r"\bUtilize\b": "Use",
        r"\bAscertain\b": "Find out",
        r"\bCommence\b": "Start",
        r"\bTerminate\b": "End"
    }

    simplified = text
    for pattern, replacement in replacements.items():
        simplified = re.sub(pattern, replacement, simplified, flags=re.IGNORECASE)

    # 🧼 Normalize spacing
    simplified = re.sub(r"\s{2,}", " ", simplified).strip()

    return simplified
