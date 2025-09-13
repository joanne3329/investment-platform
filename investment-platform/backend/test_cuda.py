import torch

print("=== PyTorch CUDA 測試 ===")

# 檢查 CUDA 是否可用
print("CUDA 可用:", torch.cuda.is_available())

if torch.cuda.is_available():
    # 顯示 GPU 名稱
    print("GPU 名稱:", torch.cuda.get_device_name(0))

    # 顯示顯卡數量
    print("GPU 數量:", torch.cuda.device_count())

    # 顯示目前 GPU id
    print("當前 GPU ID:", torch.cuda.current_device())

    # 顯示總記憶體
    total_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"總記憶體: {total_mem:.2f} GB")

    # 嘗試把 tensor 丟到 GPU
    x = torch.rand(3, 3).cuda()
    print("測試 tensor 在 GPU 上運算成功 ✅")
    print(x)
else:
    print("目前使用 CPU")
