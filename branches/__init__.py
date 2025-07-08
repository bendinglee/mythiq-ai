def init_modules(app):
    import traceback

    modules = [
        # ✅ Format: (name, route_fn, fallback_fn)
        ("qa_validator",       "routes.validate_answer_route",  "validate_answer_route"),
        ("seo_master",         "routes.optimize_keywords_route", "optimize_keywords_route"),
        ("image_generator",    "routes.generate_image_route",   "generate_image_route"),
        ("self_learning.reflection_trainer", "trainer_route.reflect_logs_route", "reflect_logs_route"),
    ]

    for module_path, route_attr, fallback in modules:
        try:
            mod = __import__(f"branches.{module_path}", fromlist=["*"])
            parts = route_attr.split(".")
            route = getattr(__import__(f"branches.{module_path}.{parts[0]}", fromlist=["*"]), parts[1])
            globals()[fallback] = route  # inject into global scope for main.py to use
            print(f"✅ Loaded: {module_path}.{route_attr}")
        except Exception as e:
            print(f"❌ Failed to load {module_path}.{route_attr}:", traceback.format_exc())
            def fallback_fn():
                return jsonify({ "success": False, "message": f"{module_path} unavailable" })
            globals()[fallback] = fallback_fn
