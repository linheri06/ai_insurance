from src.model import load_model

from src.rag import RAGRetriever
class InsuranceChatbot:
    def __init__(self, base_model, lora_model, index_dir):
        self.model, self.tokenizer = load_model(base_model, lora_model)
        self.retriever = RAGRetriever(index_dir)

    def chat(self, query, max_tokens=300):
        # 1. Retrieve context
        context_list = self.retriever.retrieve(query, top_k=7)
        context = "\n".join(context_list)

        print("\n========= DEBUG =========")
        print("QUERY:", query)
        print("CONTEXT:", context)
        print("=========================\n")

        # 2. Kiểm tra có context hay không
        use_rag = len(context.strip()) > 50

        # 3. Prompt
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
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs,
                                        max_new_tokens=max_tokens,
                                        do_sample=True,
                                        temperature=0.3,
                                        top_p=0.7,
                                        #repetition_penalty=1.2,   
                                        no_repeat_ngram_size=3   
                                    )

        raw_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        print("RAW OUTPUT:\n", raw_output)

        # 5. Clean answer (chỉ lấy phần trả lời)
        if "Trả lời:" in raw_output:
            answer = raw_output.split("Trả lời:")[-1].strip()
        else:
            answer = raw_output.strip()

        return answer