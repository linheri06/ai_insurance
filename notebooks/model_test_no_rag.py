from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

base_model_name = "Qwen/Qwen2.5-1.5B-Instruct"
lora_path = "ai_insurance/models/lora"

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

# load LoRA
model = PeftModel.from_pretrained(model, lora_path)

model.eval()

# ========================
# CHAT LOOP
# ========================
while True:
    query = input("Bạn: ")

    if query.lower() == "exit":
        break

    # ✅ Qwen dùng chat template
    messages = [
        {"role": "user", "content": query}
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print("Bot:", answer)