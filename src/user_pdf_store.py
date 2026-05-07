# src/user_pdf_store.py
# Vector store TẠM cho PDF user — tồn tại trong phiên, xóa sau

import os
import shutil


# Import hàm xử lý PDF sẵn có — chỉnh tên hàm cho khớp pdf_processing.py của bạn
from src.pdf_processing import process_pdfs  # ← đổi tên nếu khác
from src.vector_store import build_faiss_index
from src.rag import RAGRetriever

BASE_SESSION_DIR = "ai_insurance/data/sessions"
class UserPDFStore:
    def __init__(self, session_id: str):
        print(f"[UserPDFStore] Khởi tạo store cho session: {session_id}")
        self.session_id = session_id

        self.upload_dir = os.path.join(BASE_SESSION_DIR, "temp_uploads", session_id)
        self.processed_dir = os.path.join(BASE_SESSION_DIR, "processed", session_id)
        self.chunks_dir = os.path.join(BASE_SESSION_DIR, "chunks", session_id)
        self.vector_dir = os.path.join(BASE_SESSION_DIR, "vector_db", session_id)
       
       # Khởi tạo các thư mục nếu chưa tồn tại
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        os.makedirs(self.chunks_dir, exist_ok=True)
        os.makedirs(self.vector_dir, exist_ok=True)
        
        self.vectorstore = None
        self.loaded_files = []

    def add_pdf(self, file_path: str, filename: str) -> int:
        """
        Nhận file PDF, chunk và đưa vào vector store tạm.
        Trả về số chunk đã thêm.
        """
        try:
            print("Processing PDF11...", file_path)
            process_pdfs(file_path, self.processed_dir, self.chunks_dir)
        except Exception as e:
            raise ValueError(f"Lỗi khi xử lý PDF: {e}")

        print("Building FAISS index...")
        try:
            print("trc tạo faiss")
            self.vectorstore = build_faiss_index(self.chunks_dir, self.vector_dir)
            print("sau tạo faiss")
            if filename not in self.loaded_files:
                self.loaded_files.append(filename)
            print(f"Added file: {filename}")
                
            return len(os.listdir(self.chunks_dir)) 
            
        except Exception as e:
            raise RuntimeError(f"Lỗi khi tạo FAISS index: {e}")
    def search(self, query: str, k: int = 3):
        """Tìm trong PDF user đã nạp lên"""
        if self.vectorstore is None:
            return []
        try:
            retriever = RAGRetriever(self.vector_dir)
            context = retriever.retrieve(query, k=k)
            context = "\n".join(context_list)
            return context
        except Exception as e:
            raise ValueError(f"Lỗi khi xử lý PDF: {e}")

    def cleanup(self):
        """Xóa toàn bộ dữ liệu tạm sau khi phiên kết thúc"""
        # Danh sách các thư mục cần dọn dẹp của session này
        dirs_to_clean = [
            self.upload_dir,
            self.processed_dir,
            self.chunks_dir,
            self.vector_dir
        ]
        
        print(f"[UserPDF] Bắt đầu dọn dẹp dữ liệu tạm cho session: {self.session_id}")
        for folder in dirs_to_clean:
            try:
                if os.path.exists(folder):
                    shutil.rmtree(folder)
                    print(f" -> Đã xóa: {folder}")
            except Exception as e:
                print(f"[UserPDF] Lỗi khi xóa thư mục {folder}: {e}")
                
        self.vectorstore = None
        self.loaded_files = []

    def get_loaded_files(self) -> list:
        return self.loaded_files