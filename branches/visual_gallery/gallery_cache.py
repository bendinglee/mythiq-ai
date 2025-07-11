cache = []

def update_cache(entry):
    cache.append(entry)
    if len(cache) > 20:
        cache.pop(0)

def get_cached():
    return cache
