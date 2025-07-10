from branches.semantic_search.vector_store import load_index, search_index
import numpy as np

def test_vector_integrity():
    try:
        index = load_index()
        if index.ntotal == 0:
            print("⚠️ FAISS index is empty.")
            return

        # Dummy vector of correct dimension
        dim = index.d
        query = np.random.rand(dim).astype('float32')

        results = search_index(index, query, k=5)
        if results:
            print("✅ Semantic search returned matches:")
            for r in results:
                print(f"→ ID {r['id']} | Score {r['score']}")
        else:
            print("❌ No matches returned.")
    except Exception as e:
        print(f"🚨 Semantic vector test failed: {str(e)}")

if __name__ == "__main__":
    test_vector_integrity()
