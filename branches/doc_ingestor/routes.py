from flask import request, jsonify
from branches.doc_ingestor.parser import clean_and_split_text
from branches.doc_ingestor.vectorizer import append_chunks
from branches.semantic_search.embedder import embed_texts
from branches.self_learning.log import log_entry

def load_docs_route():
    data = request.get_json()
    raw_text = data.get("text", "").strip()
    if not raw_text:
        return jsonify({"success": False, "error": "No input text provided."}), 400

    chunks = clean_and_split_text(raw_text)
    added = append_chunks(chunks, source="uploaded_doc", embed_fn=embed_texts)

    # Memory log
    log_payload = {
        "input": f"[Uploaded Document] {raw_text[:120]}...",
        "output": f"Ingested {added['chunks_added']} chunks",
        "tags": ["doc_ingestion"],
        "success": True,
        "meta": {"source": "load-docs"}
    }
    with request.app.test_request_context(json=log_payload):
        log_entry(request)

    return jsonify({**added, "message": "🧠 Document ingested and indexed."})
