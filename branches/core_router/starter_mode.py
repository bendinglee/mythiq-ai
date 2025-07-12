def apply_starter_mode(response):
    return (
        "🧠 Beginner Tip: " +
        response.replace("In summary,", "")
                .replace("Therefore,", "So")
                .replace("Consequently,", "That means")
                .replace("In essence,", "Simply put,")
    )
