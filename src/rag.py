import faiss
import pickle
import numpy as np
import os

class RAGRetriever:
    def __init__(self, index_dir):
        self.index = faiss.read_index(os.path.join(index_dir, "faiss.index"))
        with open(os.path.join(index_dir, "texts.pkl"), "rb") as f:
            self.texts = pickle.load(f)

    def retrieve(self, query, top_k=3):
        from src.embedding import create_embeddings
        q_vec = np.array([create_embeddings([query])[0]]).astype("float32")
        D, I = self.index.search(q_vec, top_k)
        results = [self.texts[i] for i in I[0]]
        return results