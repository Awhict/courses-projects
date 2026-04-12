import torch
import torch.nn as nn
from config.settings import config

class TrafficTransformer(nn.Module):
    """基于Transformer的加密流量检测模型"""
    
    def __init__(self, vocab_size=256, embed_dim=64, num_heads=4, 
                 num_layers=4, hidden_dim=128, num_classes=2, max_len=512):
        super(TrafficTransformer, self).__init__()
        
        # 改进的嵌入层，考虑字节值的统计特性
        self.byte_embedding = nn.Sequential(
            nn.Embedding(vocab_size, embed_dim),
            nn.LayerNorm(embed_dim),
            nn.Dropout(0.1))
        
        self.position_embedding = nn.Embedding(max_len, embed_dim)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, 
            nhead=num_heads, 
            dim_feedforward=hidden_dim,
            dropout=config.DROPOUT_RATE,
            activation='gelu'
        )
        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layer, 
            num_layers=num_layers
        )
        
        # 使用所有位置的输出而不仅仅是第一个位置
        self.pooling = nn.AdaptiveAvgPool1d(1)
        
        self.classifier = nn.Sequential(
            nn.Linear(embed_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(config.DROPOUT_RATE),
            nn.Linear(hidden_dim, num_classes)
        )
        
    def forward(self, x):
        positions = torch.arange(0, x.size(1), dtype=torch.long, device=x.device)
        positions = positions.unsqueeze(0).expand_as(x)
        
        byte_embeds = self.byte_embedding(x)
        pos_embeds = self.position_embedding(positions)
        
        embeddings = byte_embeds + pos_embeds
        embeddings = embeddings.permute(1, 0, 2)  # [seq_len, batch, dim]
        
        transformer_output = self.transformer_encoder(embeddings)
        transformer_output = transformer_output.permute(1, 2, 0)  # [batch, dim, seq_len]
        
        # 使用平均池化代替只取第一个位置
        pooled = self.pooling(transformer_output).squeeze(-1)
        logits = self.classifier(pooled)
        
        return logits
    
    def get_attention_weights(self, x):
        """获取注意力权重（用于可视化）"""
        positions = torch.arange(0, x.size(1), dtype=torch.long, device=x.device)
        positions = positions.unsqueeze(0).expand_as(x)
        
        byte_embeds = self.byte_embedding(x)
        pos_embeds = self.position_embedding(positions)
        
        embeddings = byte_embeds + pos_embeds
        embeddings = embeddings.permute(1, 0, 2)
        
        # 存储注意力权重
        attention_weights = []
        def hook_fn(module, input, output):
            attention_weights.append(output[1])  # output[1] contains attention weights
        
        # 注册钩子
        hooks = []
        for layer in self.transformer_encoder.layers:
            hook = layer.self_attn.register_forward_hook(hook_fn)
            hooks.append(hook)
        
        # 前向传播
        _ = self.transformer_encoder(embeddings)
        
        # 移除钩子
        for hook in hooks:
            hook.remove()
            
        return attention_weights