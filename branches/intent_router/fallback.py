def fallback_to_uncertainty(text):
    return {
        "intent": "uncertain",
        "route": "uncertainty_detector",
        "message": "Confidence too low — rerouted for further analysis."
    }
