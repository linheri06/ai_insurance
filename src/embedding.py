from langchain_huggingface import HuggingFaceEmbeddings

def create_embeddings(texts, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    vectors = [embeddings.embed_query(text) for text in texts]
    return vectors