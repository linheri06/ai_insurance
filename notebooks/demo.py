# notebooks/demo_pipeline.ipynb

# 1️⃣ Import các thư viện
import os
from src.pdf_processing import process_pdfs
from src.vector_store import build_faiss_index
from src.chatbot import InsuranceChatbot

print("prensent working directory:", os.getcwd())

# 2️⃣ Đặt path
RAW_PDF_DIR = "ai_insurance/data/raw"
PROCESSED_DIR = "ai_insurance/data/processed"
CHUNKS_DIR = "ai_insurance/data/chunks"
VECTOR_DIR = "ai_insurance/data/vector_db"
LORA_MODEL_DIR = "ai_insurance/models/lora"
BASE_MODEL = "Qwen/Qwen2.5-1.5B"

# 3️⃣ Extract text + chunk PDF
print("Processing PDFs...")
process_pdfs(RAW_PDF_DIR, PROCESSED_DIR, CHUNKS_DIR)

# 4️⃣ Build FAISS index
print("Building FAISS index...")
build_faiss_index(CHUNKS_DIR, VECTOR_DIR)

# 5️⃣ Load chatbot model
print("Loading model + LoRA...")
chatbot = InsuranceChatbot(
    base_model=BASE_MODEL,
    lora_model=LORA_MODEL_DIR,
    index_dir=VECTOR_DIR
)

# 6️⃣ Test chatbot
while True:
    query = input("Bạn: ")
    if query.lower() in ["exit", "quit"]:
        break
    answer = chatbot.chat(query)
    print("Chatbot:", answer)