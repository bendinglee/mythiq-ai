def test_ingestion():
    from .parser import parse_document
    from .vectorizer import vectorize_chunks

    text = parse_document("test_files/demo.txt")
    chunks = text.split(".")[:10]
    vectors = vectorize_chunks(chunks)
    print("✅ Chunks:", len(chunks), "Vectors:", len(vectors))
