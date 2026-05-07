# src/session_manager.py

import uuid, json, os
from datetime import datetime
from src.session_vector_store import add_session_to_store
from src.user_pdf_store import UserPDFStore

SESSIONS_RAW_DIR = "ai_insurance/data/sessions/raw"

class SessionManager:
    def __init__(self, user_id: str):
        self.user_id = user_id  
        os.makedirs(SESSIONS_RAW_DIR, exist_ok=True)
        self._new_session()

    def _new_session(self):
        self.session_id = f"{self.user_id}_{str(uuid.uuid4())[:6]}"
        self.start_time = datetime.now().isoformat()
        self.messages = []
        self.pdf_store = UserPDFStore(session_id=self.session_id)
        print(f"[Session] Phiên mới: {self.session_id}")

    def add_turn(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "time": datetime.now().isoformat()
        })

    def close(self):
        """Gọi khi user kết thúc phiên"""
        if not self.messages:
            return

        session_data = {
            "session_id": self.session_id,
            "start_time": self.start_time,
            "end_time": datetime.now().isoformat(),
            "messages": self.messages
        }

        # 1. Lưu JSON gốc
        raw_path = os.path.join(SESSIONS_RAW_DIR, f"session_{self.session_id}.json")
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

        # 2. Build text và đưa vào session vector store (không đụng hệ thống)
        # text = self._build_text(session_data)
        # add_session_to_store(text, metadata={
        #     "source": "session",
        #     "session_id": self.session_id,
        #     "date": self.start_time[:10],
        #     "turns": len(self.messages)
        # })

        print(f"[Session] Đã đóng và index phiên: {self.session_id}")
        self._new_session()  # tự reset cho phiên tiếp theo

    def _build_text(self, session_data: dict) -> str:
        lines = [
            f"Phiên hội thoại ngày {session_data['start_time'][:10]}",
            f"Session ID: {session_data['session_id']}",
            "---"
        ]
        for msg in session_data["messages"]:
            prefix = "Người dùng" if msg["role"] == "user" else "Trợ lý"
            lines.append(f"{prefix}: {msg['content']}")
        return "\n".join(lines)
    
    def has_user_pdf(self):
        return len(self.pdf_store.loaded_files) > 0