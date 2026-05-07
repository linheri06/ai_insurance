from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

def load_model(base_model="Qwen/Qwen2.5-1.5B", lora_path="models/lora"):
    tokenizer = AutoTokenizer.from_pretrained(base_model)

    # load base model
    model = AutoModelForCausalLM.from_pretrained(base_model, device_map=None, torch_dtype=torch.float16, trust_remote_code=True)

    # load LoRA
    model = PeftModel.from_pretrained(model,
                                    lora_path)
    model = model.to("cuda" if torch.cuda.is_available() else "cpu")
    model = model.merge_and_unload()  # merge LoRA vào model

    model.eval()
    return model, tokenizer

# from llama_cpp import Llama

# def load_insurance_model(model_path="models/model_final_gguf/qwen2.5-1.5b.Q4_K_M.gguf"):
#     # n_ctx là độ dài ngữ cảnh, n_threads chỉnh theo số nhân CPU Xeon (ví dụ 4 hoặc 8)
#     llm = Llama(
#         model_path=model_path,
#         n_ctx=2048,
#         n_threads=4, 
#         n_gpu_layers=0 # Chạy thuần CPU
#     )
#     return llm