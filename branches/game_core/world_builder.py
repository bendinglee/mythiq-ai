def build_world(seed="mythiq_default"):
    lore = f"In the realm of {seed.title()}, neural storms reshape cities and memory acts as currency."
    factions = ["Echo Syndicate", "Neuroclave", "The Forgotten"]
    return { "seed": seed, "lore": lore, "factions": factions }
