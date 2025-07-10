metrics = {
    "requests": 0,
    "success": 0,
    "failure": 0
}

def track(result):
    metrics["requests"] += 1
    if result.get("success"):
        metrics["success"] += 1
    else:
        metrics["failure"] += 1

def get_metrics():
    return metrics
