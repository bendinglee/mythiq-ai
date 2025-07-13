from branches.dispatch_optimizer.adaptive_dispatcher import dynamic_dispatch

def test_adaptive_dispatch():
    payload = { "input": "Generate a cinematic video of a starship" }
    result = dynamic_dispatch(payload)
    assert result["routed_task"] in ["video_generation", "fallback_safe_mode"], "❌ Dispatch target invalid"
    print(f"✅ Dispatch routed to: {result['routed_task']}")

if __name__ == "__main__":
    test_adaptive_dispatch()
