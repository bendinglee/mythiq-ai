import importlib

def test_branch_init(branches):
    results = []
    for path in branches:
        try:
            branch = importlib.import_module(path)
            initialized = getattr(branch, "initialize_branch", lambda: False)()
            results.append({ "branch": path, "initialized": bool(initialized) })
        except Exception as e:
            results.append({ "branch": path, "error": str(e), "initialized": False })
    return results

if __name__ == "__main__":
    branches = [
        "branches.math_solver",
        "branches.memory_core",
        "branches.qa_validator",
        "branches.self_learning",
        "branches.semantic_search",
        "branches.seo_master",
        "branches.image_generator",
        "branches.image_synth",
        "branches.doc_ingestor",
        "branches.uncertainty_detector",
        "branches.core_router"
    ]
    results = test_branch_init(branches)
    for r in results:
        status = "✅ Initialized" if r.get("initialized") else f"❌ Failed: {r.get('error', 'Not initialized')}"
        print(f"{r['branch']} → {status}")
