import faiss
import numpy as np
import os
import pickle

def build_faiss_index(chunks_dir, index_dir):
    os.makedirs(index_dir, exist_ok=True)

    texts = []
    for filename in os.listdir(chunks_dir):
        path = os.path.join(chunks_dir, filename)
        with open(path, "r", encoding="utf-8") as file:   # ✔ đổi tên file
            texts.append(file.read())

    print("Creating embeddings...")

    from src.embedding import create_embeddings
    vectors = create_embeddings(texts)
    vectors = np.array(vectors).astype("float32")

    dim = vectors.shape[1]

    print("111111111111111111111111111")

    # ✔ dùng faiss đúng
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    faiss.write_index(index, os.path.join(index_dir, "faiss.index"))

    print("2222222222222222222222")

    with open(os.path.join(index_dir, "texts.pkl"), "wb") as file:
        pickle.dump(texts, file)

    print("FAISS index built.")



# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings

# def create_vector_db(chunks, save_path="data/vector_db"):
#     # Model này cực nhẹ, chạy tốt trên CPU Xeon
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     vector_db = FAISS.from_texts(chunks, embeddings)
#     vector_db.save_local(save_path)
#     return vector_db

# def load_vector_db(path="data/vector_db"):
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)