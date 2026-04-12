import numpy as np
import pandas as pd
import os
import torch  # 添加这行导入
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from torch.utils.data import Dataset, DataLoader
import warnings
warnings.filterwarnings('ignore')

from config.settings import config

class TrafficDataset(Dataset):
    """流量数据数据集类"""
    
    def __init__(self, sequences, labels, max_len=512):
        self.sequences = sequences
        self.labels = labels
        self.max_len = max_len
        
    def __len__(self):
        return len(self.sequences)
    
    def __getitem__(self, idx):
        sequence = self.sequences[idx]
        label = self.labels[idx]
        
        # 截断或填充序列
        if len(sequence) > self.max_len:
            sequence = sequence[:self.max_len]
        else:
            sequence = np.pad(sequence, (0, self.max_len - len(sequence)), 
                             'constant', constant_values=0)
            
        return {
            'input_ids': torch.tensor(sequence, dtype=torch.long),
            'label': torch.tensor(label, dtype=torch.long)
        }

class DataProcessor:
    """数据处理器"""
    
    @staticmethod
    def nonlinear_transform(X):
        """非线性变换将数据压缩到0-255范围"""
        X = np.arctan(X) * 2 / np.pi  # 将值压缩到[-1,1]范围
        return ((X + 1) * 127.5).astype(np.int64)  # 转换到[0,255]
    
    @staticmethod
    def augment_data(sequence):
        """数据增强"""
        if np.random.rand() > 0.5:
            idx = np.random.randint(len(sequence))
            sequence[idx] = np.clip(sequence[idx] + np.random.randint(-5,6), 0, 255)
        return sequence

class CICIDS2017Loader:
    """CIC-IDS2017 数据加载器"""
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        
    def load_data(self):
        """加载并预处理数据"""
        print("Loading and preprocessing CIC-IDS2017 data...")
        
        all_files = [f for f in os.listdir(self.data_dir) if f.endswith('.csv')]
        dfs = []
        
        for file in all_files:
            file_path = os.path.join(self.data_dir, file)
            try:
                df = pd.read_csv(file_path, encoding='utf-8', nrows=500)
                
                if df.empty:
                    print(f"File {file} is empty, skipping...")
                    continue
                    
                if len(dfs) == 0:
                    print(f"Columns in {file}: {df.columns.tolist()[:10]}...")
                
                # 确定标签
                is_malicious = 0
                attack_keywords = ['DDos', 'PortScan', 'BruteForce', 'WebAttack', 'Infiltration', 'Bot']
                if any(keyword in file for keyword in attack_keywords):
                    is_malicious = 1
                
                df['Label'] = is_malicious
                dfs.append(df)
                
            except Exception as e:
                print(f"Error loading {file}: {str(e)}")
        
        if not dfs:
            raise ValueError("No valid CSV files were loaded.")
        
        full_df = pd.concat(dfs, ignore_index=True)
        full_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        full_df.dropna(inplace=True)
        
        numeric_cols = full_df.select_dtypes(include=[np.number]).columns.tolist()
        if 'Label' in numeric_cols:
            numeric_cols.remove('Label')
        
        if not numeric_cols:
            raise ValueError("No numeric columns found for features.")
        
        X = full_df[numeric_cols]
        y = full_df['Label'].values
        
        return X, y
    
    def prepare_dataloaders(self, test_size=0.2):
        """准备训练和测试数据加载器"""
        X, y = self.load_data()
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=config.SEED, stratify=y)
        
        # 数据标准化
        scaler = RobustScaler(quantile_range=(25, 75))
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # 非线性变换
        X_train_normalized = DataProcessor.nonlinear_transform(X_train_scaled)
        X_test_normalized = DataProcessor.nonlinear_transform(X_test_scaled)
        
        # 创建数据集和数据加载器
        train_dataset = TrafficDataset(X_train_normalized, y_train, config.MAX_SEQ_LEN)
        test_dataset = TrafficDataset(X_test_normalized, y_test, config.MAX_SEQ_LEN)
        
        train_loader = DataLoader(train_dataset, batch_size=config.BATCH_SIZE, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=config.BATCH_SIZE, shuffle=False)

        # 数据验证
        self._validate_data_split(X_train_normalized, X_test_normalized, y_train, y_test)
        
        return train_loader, test_loader
    
    def _validate_data_split(self, X_train, X_test, y_train, y_test):
        """验证数据分割结果"""
        print("\n数据分割验证:")
        print(f"训练集样本数: {len(X_train)}")
        print(f"测试集样本数: {len(X_test)}")
        print(f"训练集标签分布: {np.bincount(y_train)}")
        print(f"测试集标签分布: {np.bincount(y_test)}")
        
        train_hashes = [hash(tuple(x)) for x in X_train]
        test_hashes = [hash(tuple(x)) for x in X_test]
        overlap = len(set(train_hashes) & set(test_hashes))
        print(f"训练/测试集重叠样本数: {overlap}")