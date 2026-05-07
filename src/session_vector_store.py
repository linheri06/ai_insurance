# src/session_vector_store.py
# Vector store RIÊNG cho session — không đụng đến vector_store.py hệ thống

import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings  # dùng cùng model với hệ thống

SESSION_VECTOR_DIR = "data/sessions/vector_db"

def get_session_vectorstore():
    """Trả về vector store của session — tách biệt hoàn toàn hệ thống"""
    os.makedirs(SESSION_VECTOR_DIR, exist_ok=True)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")  # chỉnh model cho khớp embedding.py

    vectorstore = Chroma(
        collection_name="user_sessions",       # tên collection riêng
        persist_directory=SESSION_VECTOR_DIR,  # thư mục riêng
        embedding_function=embeddings
    )
    return vectorstore


def add_session_to_store(text: str, metadata: dict):
    """Thêm 1 session vào store"""
    store = get_session_vectorstore()
    store.add_texts([text], metadatas=[metadata])
    store.persist()
    print(f"[SessionVectorStore] Đã lưu session: {metadata.get('session_id')}")


def search_sessions(query: str, k: int = 3):
    """Tìm kiếm trong lịch sử session của user"""
    store = get_session_vectorstore()
    results = store.similarity_search(query, k=k)
    return results