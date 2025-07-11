def index_visual(entry, gallery):
    entry["id"] = len(gallery)
    gallery.append(entry)
    return gallery
