@app.route("/api/dispatch-reflex", methods=["POST"])
def dispatch_reflex():
    from branches.feedback_loop import feedback_loop
    from branches.reflex_trainer.response_rewriter import rewrite
    from branches.reflex_trainer.emotion_tagger import tag
    from branches.cortex_fusion.task_dispatcher import dispatch
    from branches.cortex_fusion.fallback_router import reroute

    try:
        payload = request.get_json()
        enriched = feedback_loop(payload)

        output_text = enriched.get("output", "")
        emotion = tag(output_text)
        rewritten = rewrite(output_text)

        task_type = payload.get("task_type", "text")
        score = enriched.get("meta", {}).get("diagnostic_score", 0.5)
        routed = dispatch(task_type, score)

        fallback = reroute(routed) if score < 0.4 else { "fallback": routed }

        enriched["output"] = rewritten
        enriched["meta"]["emotion_tag"] = emotion
        enriched["meta"]["final_task_route"] = fallback.get("fallback")

        return jsonify({ "success": True, "result": enriched })

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
