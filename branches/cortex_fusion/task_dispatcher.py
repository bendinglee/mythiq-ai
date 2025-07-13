def dispatch(task, score=0.8):
    fallback = "fallback_router" if score < 0.4 else "core_router"
    routes = {
        "image": "image_synth",
        "video": "video_generator",
        "math": "math_solver",
        "text": "response_formatter"
    }
    return routes.get(task, fallback)
