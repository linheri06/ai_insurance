from flask import Flask, request, jsonify, render_template, session as flask_session
from werkzeug.utils import secure_filename
from src.chatbot import InsuranceChatbot
from src.session_manager import SessionManager
import os

print("__name__ =", __name__)

app = Flask(__name__)
app.secret_key = "thay_bang_random_string_bi_mat"  # bắt buộc để dùng Flask session

print("đây là app22")

chatbot = InsuranceChatbot(
    base_model="Qwen/Qwen2.5-1.5B",
    lora_model="ai_insurance/models/lora",
    index_dir="ai_insurance/data/vector_db"
)

# Lưu SessionManager theo từng user_id
user_sessions: dict[str, SessionManager] = {}  # { user_id: SessionManager }

def get_session() -> SessionManager:
    """Lấy SessionManager riêng của user hiện tại"""
    # Tự động tạo user_id nếu chưa có (lưu trong cookie)
    if "user_id" not in flask_session:
        import uuid
        flask_session["user_id"] = str(uuid.uuid4())[:8]

    user_id = flask_session["user_id"]

    # Tạo SessionManager riêng nếu user này chưa có
    if user_id not in user_sessions:
        user_sessions[user_id] = SessionManager(user_id)

    return user_sessions[user_id]


@app.route("/")
def home():
    return render_template("index2.html")


@app.route("/ask", methods=["POST"])
def ask():
    data  = request.json
    query = data.get("query")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    sess = get_session()  # ← lấy session riêng của user này
    sess.add_turn("user", query)

    user_pdf_context = ""
    if sess.has_user_pdf:
        pdf_docs = sess.pdf_store.search(query, k=3)
        if pdf_docs:
            user_pdf_context = "\n\n".join([d.page_content for d in pdf_docs])

    print("user_pdf_context:", user_pdf_context)  # debug xem context từ PDF có được đưa vào không

    if user_pdf_context:
        augmented_query = f"{query}\n\n[Tài liệu người dùng]\n{user_pdf_context}"
        answer = chatbot.chat(augmented_query)
    else:
        answer = chatbot.chat(query)

    answer = answer.split("Trả lời:")[-1].strip()
    sess.add_turn("assistant", answer)
    return jsonify({"answer": answer})


@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "Không tìm thấy file"}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({"error": "Chưa chọn file"}), 400
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Chỉ chấp nhận PDF"}), 400

    sess     = get_session()
    filename = secure_filename(file.filename)
    save_dir = f"ai_insurance/data/sessions/temp_uploads/{sess.session_id}"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    file.save(save_path)
    print(f"File '{filename}' đã được lưu tạm tại '{save_path}'")


    try:
        chunk_count = sess.pdf_store.add_pdf(save_dir, filename)
        return jsonify({
            "status":       "ok",
            "message":      f"Đã nạp '{filename}' ({chunk_count} đoạn)",
            "loaded_files": sess.pdf_store.get_loaded_files()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/end_session", methods=["POST"])
def end_session():
    sess    = get_session()
    user_id = flask_session.get("user_id")

    sess.close()  # lưu JSON + xóa PDF tạm

    # Xóa khỏi dict để giải phóng bộ nhớ
    if user_id in user_sessions:
        del user_sessions[user_id]

    flask_session.clear()
    return jsonify({"status": "ok", "message": "Phiên đã kết thúc"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)  # debug=True để tự động reload khi code thay đổi, use_reloader=False để tránh chạy 2 instance khi có nhiều file