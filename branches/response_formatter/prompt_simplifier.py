def simplify_prompt(text):
    simplified = (
        text.replace("In essence,", "")
            .replace("Herein lies", "Here is")
            .replace("It can be observed that", "We see that")
            .replace("It is known that", "We know that")
            .replace("The following exposition reveals", "Here’s what’s happening")
    )
    return simplified.strip()
