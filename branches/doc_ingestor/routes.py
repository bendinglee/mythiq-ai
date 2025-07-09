from flask import request, jsonify
from branches.doc_ingestor.parser import clean_and_split_text
from branches.doc_ingestor.vectorizer import append_chunks
from branches.semantic_search.embedder import embed_texts
from branches.self_learning.log import log_entry

def load_docs_route():
    try:
        # 📥 Step 1: Parse incoming JSON
        data = request.get_json()
        raw_text = data.get("text", "").strip()

        if not raw_text:
            return jsonify({
                "success": False,
                "error": "No input text provided."
            }), 400

        # ✂️ Step 2: Split text into clean chunks
        chunks = clean_and_split_text(raw_text)

        # 🧠 Step 3: Embed and append to vector store
        added = append_chunks(chunks, source="uploaded_doc", embed_fn=embed_texts)

        # 📝 Step 4: Log ingestion to memory
        log_payload = {
            "input": f"[Uploaded Document] {raw_text[:120]}...",
            "output": f"Ingested {added['chunks_added']} chunks",
            "tags": ["doc_ingestion"],
            "success": True,
            "meta": {
                "source": "load-docs",
                "total_chunks": added.get("chunks_added", 0)
            }
        }

        # Use context to pass log payload into `log_entry`
        with request.app.test_request_context(json=log_payload):
            log_entry(request)

        # ✅ Step 5: Return success
        return jsonify({
            **added,
            "message": "🧠 Document ingested and indexed.",
            "success": True
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
