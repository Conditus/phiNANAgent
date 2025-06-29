import torch

print("CUDA available:", torch.cuda.is_available())
print("number of GPU:", torch.cuda.device_count())
print("GPU name:", torch.cuda.get_device_name(0))

# wrote some somme comment