import torch
from torch.utils.cpp_extension import CUDA_HOME
if __name__ == '__main__':
    print(f"CUDA_HOME is set to: {CUDA_HOME}")
    print(f"Is CUDA available? {torch.cuda.is_available()}")
