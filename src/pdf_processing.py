import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pdfplumber
import re

# def extract_text_from_pdf(pdf_path):
#     reader = PdfReader(pdf_path)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text() + "\n"
#     return text

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Trong hàm process_pdfs, hãy gọi:
# text = extract_text_from_pdf(raw_path)
# text = clean_text(text)

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def chunk_text(text, chunk_size=500, chunk_overlap=250):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_text(text)
    return chunks

def process_pdfs(raw_dir, processed_dir, chunks_dir):
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(chunks_dir, exist_ok=True)

    for filename in os.listdir(raw_dir):
        if not filename.endswith(".pdf"):
            continue
        raw_path = os.path.join(raw_dir, filename)
        text = extract_text_from_pdf(raw_path)
        text = clean_text(text)

        # Save processed text
        processed_file = os.path.join(processed_dir, filename.replace(".pdf", ".txt"))
        with open(processed_file, "w", encoding="utf-8") as f:
            f.write(text)

        # Save chunks
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            chunk_file = os.path.join(chunks_dir, f"{filename}_{i}.txt")
            with open(chunk_file, "w", encoding="utf-8") as f:
                f.write(chunk)

    print("PDF processing done.")