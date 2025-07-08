tests = [
    {
        "name": "Math Solver",
        "route": "/api/solve-math",
        "payload": { "question": "What is 12*7?" },
        "check": lambda res: "84" in str(res).lower()
    },
    {
        "name": "Image Generator",
        "route": "/api/generate-image",
        "payload": { "prompt": "cyberpunk owl at night", "style": "cinematic" },
        "check": lambda res: "image_url" in res and res["image_url"]
    },
    {
        "name": "SEO Optimizer",
        "route": "/api/optimize-keywords",
        "payload": { "topic": "AI for music composition" },
        "check": lambda res: "title" in res and "AI" in res["title"]
    },
    {
        "name": "Reflection Logs",
        "route": "/api/reflect-logs",
        "payload": {},
        "check": lambda res: "success" in res
    }
]
