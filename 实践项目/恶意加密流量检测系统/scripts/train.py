import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data.data_loader import CICIDS2017Loader
from models.traffic_transformer import TrafficTransformer
from training.trainer import ModelTrainer
from training.metrics import ModelEvaluator
from utils.visualization import TrafficVisualizer
from utils.adversarial import AdversarialGenerator
from config.settings import config
import numpy as np  # 添加这行
import torch  # 添加这行
def main():
    """主训练函数"""
    print("🚀 Traffic Transformer - 恶意流量检测系统")
    print(f"使用设备: {config.DEVICE}")
    
    # 创建输出目录
    config.create_directories()
    
    # 加载数据
    print("\n📊 加载数据...")
    data_loader = CICIDS2017Loader(config.DATA_DIR)
    train_loader, test_loader = data_loader.prepare_dataloaders(test_size=config.TEST_SIZE)
    
    # 收集训练标签用于类别权重计算
    y_train_labels = []
    for batch in train_loader:
        y_train_labels.extend(batch['label'].cpu().numpy())
    y_train_labels = np.array(y_train_labels)
    
    # 初始化模型
    print("\n🧠 初始化模型...")
    model = TrafficTransformer(
        vocab_size=config.VOCAB_SIZE,
        embed_dim=config.EMBED_DIM,
        num_heads=config.NUM_HEADS,
        num_layers=config.NUM_LAYERS,
        hidden_dim=config.HIDDEN_DIM,
        num_classes=config.NUM_CLASSES,
        max_len=config.MAX_SEQ_LEN
    ).to(config.DEVICE)
    
    print(model)
    
    # 训练模型
    print("\n🎯 开始训练...")
    trainer = ModelTrainer(model, train_loader, test_loader, config.DEVICE)
    trained_model = trainer.train(epochs=config.EPOCHS, y_train_labels=y_train_labels)
    
    # 评估模型
    print("\n📈 模型评估...")
    evaluator = ModelEvaluator()
    y_true, y_pred = evaluator.evaluate_model(trained_model, test_loader, config.DEVICE)
    
    # 可视化示例
    print("\n🎨 生成可视化...")
    visualizer = TrafficVisualizer()
    sample_sequence = np.random.randint(0, 256, size=200)
    visualizer.visualize_traffic(sample_sequence, trained_model, config.DEVICE)
    
    # 测试对抗样本
    print("\n🛡️ 测试对抗样本生成...")
    original_sequence = np.random.randint(1, 256, size=100)
    original_label = 0
    target_label = 1
    
    adv_generator = AdversarialGenerator()
    adv_sequence = adv_generator.generate_adversarial_example(
        trained_model, original_sequence, target_label, config.DEVICE)
    
    # 验证对抗样本效果
    original_output = trained_model(torch.tensor(original_sequence).unsqueeze(0).to(config.DEVICE))
    adv_output = trained_model(torch.tensor(adv_sequence).unsqueeze(0).to(config.DEVICE))
    
    print(f"原始预测: {torch.argmax(original_output).item()}")
    print(f"对抗样本预测: {torch.argmax(adv_output).item()}")
    
    print("\n✅ 训练完成！")

if __name__ == "__main__":
    main()