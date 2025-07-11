from branches.intent_engine.confidence_router import reroute_low_confidence

def resolve_intent(prediction):
    if prediction["confidence"] < 0.5:
        return reroute_low_confidence(prediction)
    return prediction
