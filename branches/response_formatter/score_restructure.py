def restructure_response(response, score):
    if score < 0.4:
        return f"🔁 Revisiting answer: {response}\nLet's clarify further."
    elif score < 0.7:
        return f"📉 This may need tweaking: {response}"
    else:
        return f"✅ Well-rated reply: {response}"
