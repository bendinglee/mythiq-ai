from flask import request, jsonify
from branches.doc_ingestor.parser import clean_and_split_text
from branches.doc_ingestor.vectorizer import append_chunks
from branches.semantic_search.embedder import embed_texts
from branches.doc_ingestor.memory_writer import log_document_ingestion
from branches.self_learning.log import log_entry

def load_docs_route():
    try:
        # 📥 Step 1: Parse incoming JSON
        data = request.get_json()
        raw_text = data.get("text", "").strip()
        filename = data.get("filename", "uploaded_doc")

        if not raw_text:
            return jsonify({
                "success": False,
                "error": "No input text provided."
            }), 400

        # ✂️ Step 2: Split text into clean chunks
        chunks = clean_and_split_text(raw_text)

        # 🧠 Step 3: Embed and append to vector store
        added = append_chunks(
            chunks,
            source=filename,
            embed_fn=embed_texts
        )

        # 🗃️ Step 4: Log to long-term document memory
        log_document_ingestion(filename, chunks)

        # 📝 Step 5: Log to reflection memory core
        log_payload = {
            "input": f"[Document Upload] {raw_text[:120]}...",
            "output": f"Ingested {added['chunks_added']} chunks from '{filename}'",
            "tags": ["doc_ingestion"],
            "success": True,
            "meta": {
                "source": "load-docs",
                "total_chunks": added.get("chunks_added", 0),
                "filename": filename
            }
        }

        with request.app.test_request_context(json=log_payload):
            log_entry(request)

        # ✅ Step 6: Return success
