import json, os, datetime

LOG_PATH = "memory/docs.json"

def log_document_ingestion(filename, chunks):
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f: json.dump([], f)

    with open(LOG_PATH, "r") as f:
        logs = json.load(f)

    logs.append({
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "file": filename,
        "chunks": len(chunks),
        "source": "doc_ingestor"
    })

    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)
