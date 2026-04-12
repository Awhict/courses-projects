import torch
import numpy as np
import matplotlib.pyplot as plt
from config.settings import config

class TrafficVisualizer:
    """流量可视化工具"""
    
    @staticmethod
    def visualize_traffic(sequence, model, device):
        """
        可视化给定序列在模型中的处理过程
        """
        activations = {}
        
        def get_activation(name):
            def hook(model, input, output):
                activations[name] = output.detach()
            return hook
        
        model.eval()
        
        # 注册钩子
        model.byte_embedding.register_forward_hook(get_activation('embedding'))
        model.transformer_encoder.register_forward_hook(get_activation('transformer'))
        
        input_tensor = torch.tensor(sequence, dtype=torch.long).unsqueeze(0).to(device)
        
        with torch.no_grad():
            output = model(input_tensor)
        
        embedding = activations['embedding'].squeeze().cpu().numpy()
        embedding_shifted = embedding + 20
        transformer_out = activations['transformer'].squeeze(0).permute(1, 2, 0).cpu().numpy()
        
        # 创建图形
        plt.figure(figsize=(18, 12))
        
        # 绘制嵌入层激活
        plt.subplot(2, 1, 1)
        for i in range(min(5, embedding_shifted.shape[1])):
            plt.plot(embedding_shifted[:, i], label=f'Embedding Dimension {i}')
        plt.legend()
        plt.title('Byte Embedding Activation')
        plt.xlabel('Position in Sequence')
        plt.ylabel('Activation Value')
        
        # 绘制Transformer输出
        plt.subplot(2, 1, 2)
        for i in range(min(5, transformer_out.shape[1])):
            plt.plot(transformer_out[:, i, 0], label=f'Feature Dimension {i}')
        plt.legend()
        plt.title('Transformer Encoder Output Activation')
        plt.xlabel('Position in Sequence')
        plt.ylabel('Activation Value')
        
        plt.tight_layout()
        plt.savefig(f'{config.OUTPUT_DIR}/plots/traffic_visualization.png', dpi=300, bbox_inches='tight')
        plt.show()

    @staticmethod
    def visualize_attention(sequence, model, device):
        """可视化注意力权重"""
        model.eval()
        input_tensor = torch.tensor(sequence, dtype=torch.long).unsqueeze(0).to(device)
        
        attention_weights = model.get_attention_weights(input_tensor)
        
        # 可视化最后一层的注意力权重
        last_layer_attention = attention_weights[-1].squeeze().cpu().numpy()
        
        plt.figure(figsize=(10, 8))
        plt.imshow(last_layer_attention, cmap='viridis', aspect='auto')
        plt.colorbar()
        plt.title('Attention Weights - Last Layer')
        plt.xlabel('Key Position')
        plt.ylabel('Query Position')
        plt.tight_layout()
        plt.savefig(f'{config.OUTPUT_DIR}/plots/attention_weights.png', dpi=300, bbox_inches='tight')
        plt.show()