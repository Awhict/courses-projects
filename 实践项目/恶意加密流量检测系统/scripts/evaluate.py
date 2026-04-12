import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import torch
from data.data_loader import CICIDS2017Loader
from models.traffic_transformer import TrafficTransformer
from training.metrics import ModelEvaluator
from config.settings import config

def evaluate_saved_model():
    """评估已保存的模型"""
    print("🔍 评估已保存的模型...")
    
    # 加载数据
    data_loader = CICIDS2017Loader(config.DATA_DIR)
    _, test_loader = data_loader.prepare_dataloaders(test_size=config.TEST_SIZE)
    
    # 初始化模型
    model = TrafficTransformer(
        vocab_size=config.VOCAB_SIZE,
        embed_dim=config.EMBED_DIM,
        num_heads=config.NUM_HEADS,
        num_layers=config.NUM_LAYERS,
        hidden_dim=config.HIDDEN_DIM,
        num_classes=config.NUM_CLASSES,
        max_len=config.MAX_SEQ_LEN
    ).to(config.DEVICE)
    
    # 加载保存的权重
    if os.path.exists(config.MODEL_SAVE_PATH):
        model.load_state_dict(torch.load(config.MODEL_SAVE_PATH, map_location=config.DEVICE))
        print("✅ 模型权重加载成功")
    else:
        print("❌ 未找到保存的模型文件")
        return
    
    # 评估模型
    evaluator = ModelEvaluator()
    y_true, y_pred = evaluator.evaluate_model(model, test_loader, config.DEVICE)
    
    print("✅ 评估完成")

if __name__ == "__main__":
    evaluate_saved_model()