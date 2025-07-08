print("🔁 Initializing fallback-safe modules...")

def init_modules(app):
    import traceback
    print("📦 Beginning dynamic module injection...")

    modules = [
        # ✅ Format: (module_path, route_function_path, global_name)
        ("qa_validator",       "routes.validate_answer_route",      "validate_answer_route"),
        ("seo_master",         "routes.optimize_keywords_route",    "optimize_keywords_route"),
        ("image_generator",    "routes.generate_image_route",       "generate_image_route"),
        ("self_learning.reflection_trainer", "trainer_route.reflect_logs_route", "reflect_logs_route"),
    ]

    for module_path, route_attr, global_name in modules:
        try:
            print(f"📥 Trying: {module_path}.{route_attr}")
            mod = __import__(f"branches.{module_path}", fromlist=["*"])
            parts = route_attr.split(".")
            route_module = __import__(f"branches.{module_path}.{parts[0]}", fromlist=["*"])
            route = getattr(route_module, parts[1])
            globals()[global_name] = route
            print(f"✅ Loaded: {module_path}.{route_attr} → {global_name}")
        except Exception as e:
            print(f"❌ Failed to load {module_path}.{route_attr}:", traceback.format_exc())

            def fallback_fn():
                return jsonify({ "success": False, "message": f"{module_path} unavailable" })
            globals()[global_name] = fallback_fn

    print("✅ Fallback-safe injection complete.")
