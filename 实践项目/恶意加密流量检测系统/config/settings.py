import torch
import os

class Config:
    """项目配置类"""
    
    # 基础设置
    SEED = 42
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # 数据设置
    DATA_DIR = r"E:\Project\Python\PythonProject\BERT\data\datasets"
    MAX_SEQ_LEN = 512
    TEST_SIZE = 0.2
    BATCH_SIZE = 32
    
    # 模型架构
    VOCAB_SIZE = 256
    EMBED_DIM = 64
    NUM_HEADS = 4
    NUM_LAYERS = 4
    HIDDEN_DIM = 128
    NUM_CLASSES = 2
    DROPOUT_RATE = 0.2
    
    # 训练参数
    LEARNING_RATE = 3e-4
    WEIGHT_DECAY = 3e-4
    EPOCHS = 10
    WARMUP_STEPS = None  # 自动计算
    
    # 路径设置
    OUTPUT_DIR = "outputs"
    MODEL_SAVE_PATH = "outputs/models/best_model.pth"
    
    @classmethod
    def create_directories(cls):
        """创建必要的目录"""
        os.makedirs(f"{cls.OUTPUT_DIR}/models", exist_ok=True)
        os.makedirs(f"{cls.OUTPUT_DIR}/plots", exist_ok=True)

config = Config()