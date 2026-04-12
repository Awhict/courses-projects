import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import torch
import numpy as np
from data.data_loader import DataProcessor
from models.traffic_transformer import TrafficTransformer
from config.settings import config
import base64
from io import BytesIO
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
import tempfile
import json

# 获取当前文件（app.py）的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 设置模板和静态文件目录 - 修正路径
template_dir = os.path.join(current_dir, '../frontend/templates')
static_dir = os.path.join(current_dir, '../frontend/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app)

# 全局变量存储模型
model = None

def load_model():
    """加载训练好的模型"""
    global model
    model = TrafficTransformer(
        vocab_size=config.VOCAB_SIZE,
        embed_dim=config.EMBED_DIM,
        num_heads=config.NUM_HEADS,
        num_layers=config.NUM_LAYERS,
        hidden_dim=config.HIDDEN_DIM,
        num_classes=config.NUM_CLASSES,
        max_len=config.MAX_SEQ_LEN
    ).to(config.DEVICE)
    
    if os.path.exists(config.MODEL_SAVE_PATH):
        model.load_state_dict(torch.load(config.MODEL_SAVE_PATH, map_location=config.DEVICE))
        model.eval()
        return True
    return False

# 初始化加载模型
model_loaded = load_model()

# 修正路由配置 - 添加所有页面的路由
@app.route('/')
@app.route('/index.html')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/model')
@app.route('/model.html')
def model_page():
    """模型架构页面"""
    return render_template('model.html')

@app.route('/detection')
@app.route('/detection.html')
def detection_page():
    """实时检测页面"""
    return render_template('detection.html')

@app.route('/visualization')
@app.route('/visualization.html')
def visualization_page():
    """数据可视化页面"""
    return render_template('visualization.html')

@app.route('/results')
@app.route('/results.html')
def results_page():
    """实验结果页面"""
    return render_template('results.html')

@app.route('/api/status', methods=['GET'])
def get_status():
    """获取系统状态"""
    return jsonify({
        'model_loaded': model_loaded,
        'device': str(config.DEVICE),
        'classes': ['正常流量', '恶意流量']
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """预测流量类型"""
    if not model_loaded:
        return jsonify({'error': '模型未加载成功'}), 500
    
    try:
        data = request.json
        sequence = np.array(data['sequence'], dtype=np.int64)
        
        # 数据预处理
        if len(sequence) > config.MAX_SEQ_LEN:
            sequence = sequence[:config.MAX_SEQ_LEN]
        else:
            sequence = np.pad(sequence, (0, config.MAX_SEQ_LEN - len(sequence)), 
                             'constant', constant_values=0)
        
        # 转换为tensor并预测
        input_tensor = torch.tensor(sequence, dtype=torch.long).unsqueeze(0).to(config.DEVICE)
        
        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.softmax(output, dim=1).cpu().numpy()[0]
            predicted_class = int(torch.argmax(output).item())
        
        # 生成可视化
        viz_plot = generate_visualization(sequence)
        
        return jsonify({
            'predicted_class': predicted_class,
            'class_name': ['正常流量', '恶意流量'][predicted_class],
            'probabilities': {
                '正常流量': float(probabilities[0]),
                '恶意流量': float(probabilities[1])
            },
            'visualization': viz_plot
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/pcap_upload', methods=['POST'])
def pcap_upload():
    """处理PCAP文件上传和批量检测"""
    if not model_loaded:
        return jsonify({'error': '模型未加载成功'}), 500
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有文件被上传'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        if not (file.filename.endswith('.pcap') or file.filename.endswith('.pcapng')):
            return jsonify({'error': '只支持PCAP或PCAPNG文件'}), 400
        
        # 保存上传的文件到临时目录
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pcap') as temp_file:
            file.save(temp_file.name)
            temp_filename = temp_file.name
        
        try:
            # 模拟PCAP文件解析和流量提取
            # 在实际应用中，这里应该使用scapy或类似的库来解析PCAP文件
            simulated_flows = simulate_pcap_parsing(temp_filename)
            
            # 批量预测
            results = []
            for flow in simulated_flows:
                sequence = np.array(flow['packet_lengths'], dtype=np.int64)
                
                # 数据预处理
                if len(sequence) > config.MAX_SEQ_LEN:
                    sequence = sequence[:config.MAX_SEQ_LEN]
                else:
                    sequence = np.pad(sequence, (0, config.MAX_SEQ_LEN - len(sequence)), 
                                     'constant', constant_values=0)
                
                # 转换为tensor并预测
                input_tensor = torch.tensor(sequence, dtype=torch.long).unsqueeze(0).to(config.DEVICE)
                
                with torch.no_grad():
                    output = model(input_tensor)
                    probabilities = torch.softmax(output, dim=1).cpu().numpy()[0]
                    predicted_class = int(torch.argmax(output).item())
                
                results.append({
                    'src_ip': flow['src_ip'],
                    'dst_ip': flow['dst_ip'],
                    'src_port': flow['src_port'],
                    'dst_port': flow['dst_port'],
                    'protocol': flow['protocol'],
                    'predicted_class': predicted_class,
                    'class_name': ['正常流量', '恶意流量'][predicted_class],
                    'normal_probability': float(probabilities[0]),
                    'malicious_probability': float(probabilities[1])
                })
            
            # 统计信息
            total_flows = len(results)
            malicious_flows = sum(1 for r in results if r['predicted_class'] == 1)
            
            return jsonify({
                'results': results,
                'summary': {
                    'total_flows': total_flows,
                    'malicious_flows': malicious_flows,
                    'normal_flows': total_flows - malicious_flows,
                    'malicious_percentage': (malicious_flows / total_flows * 100) if total_flows > 0 else 0
                }
            })
            
        finally:
            # 清理临时文件
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
                
    except Exception as e:
        return jsonify({'error': f'文件处理失败: {str(e)}'}), 500

def simulate_pcap_parsing(pcap_file_path):
    """模拟PCAP文件解析，返回流量数据列表"""
    # 在实际应用中，这里应该使用scapy来解析PCAP文件
    # 这里我们返回模拟数据用于演示
    
    import random
    flows = []
    
    # 生成一些模拟流量数据
    protocols = ['TCP', 'UDP', 'ICMP']
    for i in range(random.randint(5, 15)):
        flow = {
            'src_ip': f'192.168.1.{random.randint(1, 254)}',
            'dst_ip': f'10.0.0.{random.randint(1, 254)}',
            'src_port': random.randint(1024, 65535),
            'dst_port': random.choice([80, 443, 22, 53, 3389]),
            'protocol': random.choice(protocols),
            'packet_lengths': [random.randint(64, 1500) for _ in range(random.randint(10, 50))]
        }
        flows.append(flow)
    
    return flows

def generate_visualization(sequence):
    """生成流量可视化图像"""
    try:
        # 创建简单的可视化图表
        plt.figure(figsize=(10, 6))
        
        # 绘制序列数据
        plt.subplot(2, 1, 1)
        plt.plot(sequence[:50], 'b-', alpha=0.7)
        plt.title('流量序列数据 (前50个数据点)')
        plt.xlabel('序列位置')
        plt.ylabel('数据值')
        plt.grid(True, alpha=0.3)
        
        # 绘制统计信息
        plt.subplot(2, 1, 2)
        stats_data = [len(sequence), np.mean(sequence), np.std(sequence), np.max(sequence)]
        stats_labels = ['序列长度', '平均值', '标准差', '最大值']
        plt.bar(stats_labels, stats_data, color=['#165DFF', '#36CFC9', '#52C41A', '#FF4D4F'])
        plt.title('序列统计信息')
        plt.ylabel('数值')
        
        plt.tight_layout()
        
        # 保存到内存
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        
        # 转换为base64
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()
        
        return img_base64
    except Exception as e:
        print(f"可视化生成错误: {str(e)}")
        return None

if __name__ == '__main__':
    # 确保模板和静态文件目录存在
    os.makedirs(template_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)
    
    print(f"模板目录: {template_dir}")
    print(f"静态文件目录: {static_dir}")
    print("启动Flask应用...")
    
    app.run(host='0.0.0.0', port=5000, debug=True)