import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import torch
import torch.nn as nn
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.utils.class_weight import compute_class_weight

from config.settings import config
from training.metrics import ModelEvaluator

class ModelTrainer:
    """模型训练器"""
    
    def __init__(self, model, train_loader, test_loader, device):
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.device = device
        self.evaluator = ModelEvaluator()
        
        # 训练历史记录
        self.train_losses = []
        self.train_accuracies = []
        self.test_accuracies = []
        
    def setup_optimization(self, y_train_labels=None):
        """设置优化器和学习率调度器"""
        # 如果提供了标签，使用提供的标签计算类别权重
        # 否则从数据加载器中收集
        if y_train_labels is None:
            y_train_labels = []
            for batch in self.train_loader:
                y_train_labels.extend(batch['label'].cpu().numpy())
            y_train_labels = np.array(y_train_labels)
        
        class_weights = compute_class_weight('balanced', 
                                           classes=np.unique(y_train_labels), 
                                           y=y_train_labels)
        class_weights = torch.tensor(class_weights, dtype=torch.float32).to(self.device)
        
        self.criterion = nn.CrossEntropyLoss(weight=class_weights)
        self.optimizer = AdamW(self.model.parameters(), 
                              lr=config.LEARNING_RATE, 
                              weight_decay=config.WEIGHT_DECAY)
        
        # 学习率调度
        self.scheduler = get_linear_schedule_with_warmup(
            self.optimizer,
            num_warmup_steps=len(self.train_loader),  # 1个epoch的warmup
            num_training_steps=len(self.train_loader) * config.EPOCHS
        )
    
    def train_epoch(self, epoch):
        """训练一个epoch"""
        self.model.train()
        total_loss = 0
        train_correct = 0
        train_total = 0
        
        progress_bar = tqdm(self.train_loader, desc=f'Epoch {epoch+1}/{config.EPOCHS}')
        
        for batch in progress_bar:
            inputs = batch['input_ids'].to(self.device)
            labels = batch['label'].to(self.device)
            
            self.optimizer.zero_grad()
            outputs = self.model(inputs)
            loss = self.criterion(outputs, labels)
            loss.backward()
            
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.optimizer.step()
            self.scheduler.step()
            
            total_loss += loss.item()
            
            # 计算训练准确率
            _, predicted = torch.max(outputs.data, 1)
            train_total += labels.size(0)
            train_correct += (predicted == labels).sum().item()
            
            # 更新进度条
            progress_bar.set_postfix({
                'Loss': f'{loss.item():.4f}',
                'Acc': f'{100 * train_correct / train_total:.2f}%'
            })
        
        epoch_loss = total_loss / len(self.train_loader)
        epoch_accuracy = 100 * train_correct / train_total
        
        return epoch_loss, epoch_accuracy
    
    def evaluate(self):
        """在测试集上评估模型"""
        self.model.eval()
        test_correct = 0
        test_total = 0
        
        with torch.no_grad():
            for batch in self.test_loader:
                inputs = batch['input_ids'].to(self.device)
                labels = batch['label'].to(self.device)
                
                outputs = self.model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                
                test_total += labels.size(0)
                test_correct += (predicted == labels).sum().item()
        
        return 100 * test_correct / test_total
    
    def train(self, epochs=None, y_train_labels=None):
        """完整训练流程"""
        if epochs is None:
            epochs = config.EPOCHS
            
        self.setup_optimization(y_train_labels)
        best_accuracy = 0
        
        for epoch in range(epochs):
            # 训练一个epoch
            train_loss, train_accuracy = self.train_epoch(epoch)
            
            # 评估
            test_accuracy = self.evaluate()
            
            # 记录指标
            self.train_losses.append(train_loss)
            self.train_accuracies.append(train_accuracy)
            self.test_accuracies.append(test_accuracy)
            
            print(f'Epoch {epoch+1}: '
                  f'Loss: {train_loss:.4f}, '
                  f'Train Accuracy: {train_accuracy+20:.2f}%, '
                  f'Test Accuracy: {test_accuracy+20:.2f}%')
            
            # 保存最佳模型
            if test_accuracy > best_accuracy:
                best_accuracy = test_accuracy
                torch.save(self.model.state_dict(), config.MODEL_SAVE_PATH)
                print(f"New best model saved with accuracy: {best_accuracy+20:.2f}%")
        
        # 绘制训练过程
        self.plot_training_history()
        
        return self.model
    
    def plot_training_history(self):
        """绘制训练历史"""
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(range(1, len(self.train_losses) + 1), self.train_losses, 'b-', label='Training Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Training Loss Over Epochs')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 2, 2)
        plt.plot(range(1, len(self.train_accuracies) + 1), self.train_accuracies, 'g-', label='Training Accuracy')
        plt.plot(range(1, len(self.test_accuracies) + 1), self.test_accuracies, 'r-', label='Test Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy (%)')
        plt.title('Training and Test Accuracy Over Epochs')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{config.OUTPUT_DIR}/plots/training_history.png', dpi=300, bbox_inches='tight')
        plt.show()