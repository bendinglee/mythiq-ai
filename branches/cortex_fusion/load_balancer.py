import random

def balance(task_type):
    pool = {
        "image": ["image_synth_a", "image_synth_b"],
        "video": ["video_gen_a", "video_gen_b"]
    }
    return random.choice(pool.get(task_type, ["core_router"]))
