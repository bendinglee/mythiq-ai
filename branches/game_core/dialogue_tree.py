def generate_dialogue(npc):
    return {
        "npc": npc,
        "dialogue": {
            "intro": f"Greetings, I am {npc}.",
            "choices": [
                { "player": "Who are you?", "response": f"I am one who remembers." },
                { "player": "What can I do here?", "response": "Change the past if you choose." }
            ]
        }
    }
