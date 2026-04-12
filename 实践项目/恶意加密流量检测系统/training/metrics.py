import torch
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from config.settings import config

class ModelEvaluator:
    """模型评估器"""
    
    def __init__(self):
        pass
    
    def evaluate_model(self, model, loader, device):
        """全面评估模型性能"""
        model.eval()
        y_true, y_pred = [], []
        
        with torch.no_grad():
            for batch in loader:
                inputs = batch['input_ids'].to(device)
                labels = batch['label'].to(device)
                
                outputs = model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                
                y_true.extend(labels.cpu().numpy())
                y_pred.extend(predicted.cpu().numpy())
        
        # 计算混淆矩阵
        cm = confusion_matrix(y_true, y_pred)
        
        # 可视化混淆矩阵
        self.plot_confusion_matrix(cm)
        
        # 打印详细报告
        print("Confusion Matrix:")
        print(cm)
        print("\nClassification Report:")
        print(classification_report(y_true, y_pred, 
                                  target_names=['正常流量', '恶意流量']))
        
        return y_true, y_pred
    
    def plot_confusion_matrix(self, cm):
        """绘制混淆矩阵"""
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['正常流量', '恶意流量'], 
                   yticklabels=['正常流量', '恶意流量'])
        plt.title('混淆矩阵')
        plt.xlabel('预测标签')
        plt.ylabel('真实标签')
        plt.tight_layout()
        plt.savefig(f'{config.OUTPUT_DIR}/plots/confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()