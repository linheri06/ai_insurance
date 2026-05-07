from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from src.rag import RAGRetriever

base_model_name = "Qwen/Qwen2.5-1.5B"
# lora_path = "ai_insurance/models/lora"

# ✅ load tokenizer từ base model
tokenizer = AutoTokenizer.from_pretrained(base_model_name)

# fix pad token
tokenizer.pad_token = tokenizer.eos_token

# load base model
model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
retriever = RAGRetriever("ai_insurance/data/vector_db")
model.eval()

# ========================
# CHAT LOOP
# ========================
while True:
    query = input("Bạn: ")

    if query.lower() == "exit":
        break

    # ✅ Qwen dùng chat template
    context_list = retriever.retrieve(query, top_k=5)
    context = "\n".join(context_list)
    messages = [
        {"role": "user", "content": query}
    ]

    prompt = f"""Bạn là chatbot tư vấn bảo hiểm.

                        LUẬT:
                        - Trả lời dựa trên CONTEXT
                        - Trả lời đầy đủ, rõ ràng, không có thông tin thừa

                        CONTEXT:
                        {context}

                        Câu hỏi: {query}
                        Trả lời:
                        """

    # 4. Generate
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs,
                                    max_new_tokens=200,
                                    do_sample=True,
                                    temperature=0.3,
                                    top_p=0.7,
                                    repetition_penalty=1.2,   
                                    no_repeat_ngram_size=3    
                                )


    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print("Bot:", answer)