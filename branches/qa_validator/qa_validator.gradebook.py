def log_grade(payload, result=None, return_only=False):
    if result is None:
        from branches.qa_validator.scorer import score_response
        result = score_response(payload)

    if return_only:
        return result

    # If not return_only, continue logging to memory
    from branches.self_learning.log import log_entry
    enriched = { **payload, "meta": result }
    log_entry(enriched)
    return result
