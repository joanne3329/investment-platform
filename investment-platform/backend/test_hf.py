from transformers import pipeline
import torch

print("Torch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("使用 GPU:", torch.cuda.get_device_name(0))
else:
    print("目前在用 CPU")

# 載入中文小模型（輕量版，適合 CPU）
generator = pipeline(
    "text-generation",
    model="uer/gpt2-chinese-cluecorpussmall",
    device=0 if torch.cuda.is_available() else -1
)


# 測試問題
query = "請解釋什麼是股票"
result = generator(query, max_length=50, num_return_sequences=1)
print("\n=== 模型回覆 ===")
print(result[0]["generated_text"])
