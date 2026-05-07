from flask import Flask, request, jsonify, render_template
from src.chatbot import InsuranceChatbot
import os

print("đây là app")
app = Flask(__name__)

print("present working directory:", os.getcwd())

chatbot = InsuranceChatbot(
    base_model="Qwen/Qwen2.5-1.5B",
    lora_model="ai_insurance/models/lora",
    index_dir="ai_insurance/data/vector_db"
)

@app.route("/")
def home():
    return render_template("index.html")



# 👉 API chatbot
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    query = data.get("query")

    if not query:
        return jsonify({"error": "Missing query"}), 400

    answer = chatbot.chat(query)
    answer = answer.split("Trả lời:")[-1].strip()
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)