import torch

def main():
    print(f"PyTorch version: {torch.__version__}")
    print("CUDA Available:", torch.cuda.is_available())

if __name__ == "__main__":
    main()
