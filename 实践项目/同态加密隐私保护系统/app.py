import os
import traceback
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tenseal as ts
import base64
from datetime import datetime
from homomorphic_encryption.BGV import BGV, PrivacyPreservingSalarySystem
from homomorphic_encryption.BFV import BFVCryptoSystem
from homomorphic_encryption.CKKS import CKKSComparator as ckks_compare
from homomorphic_encryption.TFHE import TFHEParameters, TLWE, TRLWE, TRGSW, FloatEncoder
from homomorphic_encryption.FHEW import SEALBooleanEncryptor

app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_html():
    return send_from_directory(os.path.dirname(__file__), 'index.html')

# 确保静态文件路由正确
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# BGV 路由接口
# 初始化隐私保护的工资系统
bgv_salary_system = PrivacyPreservingSalarySystem()

@app.route('/add_employee_bgv', methods=['POST'])
def add_employee_bgv():
    """添加员工及其工资（BGV）"""
    name = request.form.get('name')
    salary = int(request.form.get('salary'))
    
    # 添加员工并加密其工资
    bgv_salary_system.add_employee(name, salary)
    
    # 打印员工姓名和工资到终端
    app.logger.info(f"员工{name}的工资（BGV）已添加并加密，工资为{salary}")
    
    return jsonify({"message": f"员工{name}的工资（BGV）已添加并加密！"}), 200

@app.route('/bgv_compare_salaries', methods=['POST'])
def bgv_compare_salaries():
    """比较两位员工的工资（BGV）"""
    name1 = request.form.get('name1')
    name2 = request.form.get('name2')
    
    # 使用同态加密进行工资比较
    comparison_result = bgv_salary_system.compare_salaries(name1, name2)
    
    return jsonify({"result": comparison_result}), 200

@app.route('/decrypt_salary_bgv', methods=['POST'])
def decrypt_salary_bgv():
    """解密工资（BGV）"""
    name = request.form.get('name')
    
    # 获取加密工资并解密
    encrypted_salary = bgv_salary_system.get_encrypted_salary(name)
    decrypted_salary = bgv_salary_system.decrypt_salary(encrypted_salary)
    
    return jsonify({"salary": decrypted_salary}), 200

# BFV 部分
bfv_system = BFVCryptoSystem()
bfv_system.generate_keys()

@app.route('/add_employee_bfv', methods=['POST'])
def add_employee_bfv():
    """添加员工及其工资（BFV）"""
    name = request.form.get('name')
    salary = int(request.form.get('salary'))
    try:
        bfv_system.encrypt(name, salary)
        app.logger.info(f"员工{name}的工资（BFV）已添加并加密，工资为{salary}")
        return jsonify({"message": f"员工{name}的工资（BFV）已添加并加密！"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/bfv_compare_salaries', methods=['POST'])
def bfv_compare_salaries():
    """比较两位员工的工资（BFV）"""
    name1 = request.form.get('name1')
    name2 = request.form.get('name2')
    try:
        result, _ = bfv_system.compare(name1, name2)
        if result == 1:
            return jsonify({"result": f"{name1}的工资高于{name2}"}), 200
        elif result == -1:
            return jsonify({"result": f"{name1}的工资低于{name2}"}), 200
        else:
            return jsonify({"result": f"{name1}和{name2}的工资相等"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/decrypt_salary_bfv', methods=['POST'])
def decrypt_salary_bfv():
    """解密工资（BFV）"""
    name = request.form.get('name')
    try:
        decrypted_salary = bfv_system.decrypt(name)
        return jsonify({"salary": decrypted_salary}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# FHEW部分
app.secret_key = 'your-secret-key-here'

DATA_FOLDER = "encrypted_FHEW"
os.makedirs(DATA_FOLDER, exist_ok=True)

fhew_encryptor = SEALBooleanEncryptor()

@app.route('/api/files', methods=['GET'])
def get_files():
    encrypted_files = []
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".txt") and "_encrypted_" in filename:
            parts = filename.split("_encrypted_")
            employee_name = parts[0]
            date_str = parts[1].replace(".txt", "")
            encrypted_files.append({
                "filename": filename,
                "employee": employee_name,
                "date": date_str
            })
    return jsonify(encrypted_files)

@app.route('/api/encrypt', methods=['POST'])
def encrypt_salary():
    data = request.json
    name = data.get('name', '').strip()
    salary = data.get('salary', 0)
    
    if not name:
        return jsonify({"error": "请输入员工姓名"}), 400
    
    try:
        encrypted_salary = fhew_encryptor.encrypt_integer(salary)
        encrypted_data = [
            base64.b64encode(cipher.serialize()).decode("utf-8")
            for cipher in encrypted_salary
        ]

        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_encrypted_{now}.txt"
        filepath = os.path.join(DATA_FOLDER, filename)

        with open(filepath, "w") as f:
            f.write("\n".join(encrypted_data))

        return jsonify({
            "success": True,
            "filename": filename,
            "employee": name,
            "date": now
        })
    except Exception as e:
        return jsonify({"error": f"加密过程中发生错误: {str(e)}"}), 500

@app.route('/api/compare', methods=['POST'])
def fhew_compare_salaries():
    data = request.json
    file1 = data.get('file1')
    file2 = data.get('file2')
    
    if not file1 or not file2:
        return jsonify({"error": "请选择两个文件进行比较"}), 400
    
    if file1 == file2:
        return jsonify({"error": "不能选择相同的文件进行比较"}), 400
    
    try:
        with open(os.path.join(DATA_FOLDER, file1), "r") as f:
            encrypted_data1 = f.read().splitlines()
        with open(os.path.join(DATA_FOLDER, file2), "r") as f:
            encrypted_data2 = f.read().splitlines()

        # 解密回整数值进行简单比较
        a_bits = [ts.bfv_vector_from(fhew_encryptor.context, base64.b64decode(d)) for d in encrypted_data1]
        b_bits = [ts.bfv_vector_from(fhew_encryptor.context, base64.b64decode(d)) for d in encrypted_data2]
        
        plain1 = fhew_encryptor.decrypt_integer(a_bits)
        plain2 = fhew_encryptor.decrypt_integer(b_bits)
        
        debug_info = {
            "a_bits": fhew_encryptor.debug_decrypt_bits(a_bits),
            "b_bits": fhew_encryptor.debug_decrypt_bits(b_bits)
        }

        if plain1 > plain2:
            return jsonify({"result": 1, "debug_info": debug_info})
        elif plain1 < plain2:
            return jsonify({"result": -1, "debug_info": debug_info})
        else:
            return jsonify({"result": 0, "debug_info": debug_info})
            
    except Exception as e:
        return jsonify({"error": f"比较过程中发生错误: {str(e)}"}), 500

# CKKS 部分
CKKS_DATA_DIR = "ckks_data"

if not os.path.exists(CKKS_DATA_DIR):
    os.makedirs(CKKS_DATA_DIR)
    # print(f"创建了CKKS数据目录: {CKKS_DATA_DIR}")
else:
    # print(f"使用现有CKKS数据目录: {CKKS_DATA_DIR}")
    pass

# 初始化CKKS上下文
ckks_context = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=8192,
    coeff_mod_bit_sizes=[60, 40, 40, 60]
)
ckks_context.generate_galois_keys()
ckks_context.global_scale = 2**40

@app.route('/add_employee_ckks', methods=['POST'])
def add_employee_ckks():
    try:
        name = request.form.get('name')
        salary = request.form.get('salary')
        
        app.logger.info(f"尝试添加员工: {name}, 工资: {salary}")
        
        if not name:
            return jsonify({"error": "请提供员工姓名"}), 400
            
        try:
            salary = float(salary)
        except (ValueError, TypeError):
            return jsonify({"error": "工资必须是数字"}), 400
            
        # 确保CKKS上下文已初始化
        if not hasattr(app, 'ckks_context'):
            app.ckks_context = ts.context(
                ts.SCHEME_TYPE.CKKS,
                poly_modulus_degree=8192,
                coeff_mod_bit_sizes=[60, 40, 40, 60]
            )
            app.ckks_context.generate_galois_keys()
            app.ckks_context.global_scale = 2**40
            
        # 加密工资
        encrypted_salary = ts.ckks_vector(app.ckks_context, [salary])
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}.ckks"
        filepath = os.path.join(CKKS_DATA_DIR, filename)
        
        app.logger.info(f"保存加密文件: {filepath}")
        
        # 正确保存加密数据：先序列化，再写入文件
        encrypted_bytes = encrypted_salary.serialize()
        with open(filepath, 'wb') as f:
            f.write(encrypted_bytes)
        
        return jsonify({
            "success": True,
            "message": f"员工{name}的工资（CKKS）已加密并保存",
            "filename": filename
        }), 200
        
    except Exception as e:
        import traceback
        app.logger.error(f"添加员工失败: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "error": f"服务器内部错误: {str(e)}"
        }), 500

@app.route('/ckks_get_files', methods=['GET'])
def ckks_get_files():
    try:
        files = []
        for filename in os.listdir(CKKS_DATA_DIR):
            if filename.endswith('.ckks'):
                name_parts = filename.split('_')
                name = '_'.join(name_parts[:-1])
                timestamp = name_parts[-1].replace('.ckks', '')
                files.append({
                    'filename': filename,
                    'name': name,
                    'timestamp': timestamp
                })
        return jsonify(files)
    except Exception as e:
        app.logger.error(f"获取CKKS文件列表失败: {str(e)}")
        return jsonify({"error": f"获取文件列表失败: {str(e)}"}), 500

@app.route('/ckks_compare_salaries', methods=['POST'])
def ckks_compare_salaries():
    file1 = request.form.get('file1')
    file2 = request.form.get('file2')
    
    if not file1 or not file2:
        return jsonify({"error": "请选择两个文件进行比较"}), 400
    
    file1_path = os.path.join(CKKS_DATA_DIR, file1)
    file2_path = os.path.join(CKKS_DATA_DIR, file2)
    
    if not os.path.exists(file1_path) or not os.path.exists(file2_path):
        return jsonify({"error": "文件不存在"}), 400
    
    try:
        # 正确加载加密数据：先读取文件，再反序列化
        with open(file1_path, 'rb') as f:
            encrypted1_bytes = f.read()
        encrypted1 = ts.ckks_vector_from(app.ckks_context, encrypted1_bytes)
        
        with open(file2_path, 'rb') as f:
            encrypted2_bytes = f.read()
        encrypted2 = ts.ckks_vector_from(app.ckks_context, encrypted2_bytes)
        
        # 同态比较（使用CKKS的近似比较）
        # 这里使用减法和符号函数的近似
        diff = encrypted1 - encrypted2
        
        # 为了简化，我们在这里解密结果进行比较（实际应用中应该使用更复杂的同态操作）
        decrypted_diff = diff.decrypt()[0]
        
        if decrypted_diff > 0:
            result = "第一个工资高于第二个"
        elif decrypted_diff < 0:
            result = "第一个工资低于第二个"
        else:
            result = "两个工资相等"
            
        return jsonify({"result": result}), 200
    except Exception as e:
        app.logger.error(f"比较工资失败: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": f"比较过程中发生错误: {str(e)}"}), 500

from typing import Tuple
import numpy as np

# TFHE部分
tfhe_params = TFHEParameters(n=500, N=1024, k=1, l=2, Bgbit=10, Bg=1024, sigma=0.01, sigma_min=0.001, h=100)
tfhe_encoder = FloatEncoder()
tfhe_tlwe = TLWE(tfhe_params, tfhe_encoder)
tfhe_trlwe = TRLWE(tfhe_params, tfhe_encoder)
tfhe_trgsw = TRGSW(tfhe_params)

# 存储员工加密工资的字典
tfhe_employees = {}

# 添加浮点数的同态运算函数
def tfhe_float_add(ciphertext1: Tuple[np.ndarray, float], ciphertext2: Tuple[np.ndarray, float]) -> Tuple[np.ndarray, float]:
    """同态加法运算（TLWE）"""
    a1, b1 = ciphertext1
    a2, b2 = ciphertext2
    # 密文相加
    a_result = a1 + a2
    b_result = b1 + b2  # 简化版，实际应使用Torus.add
    return (a_result, b_result)

# 修改后的同态比较函数
def tfhe_float_compare(ciphertext1: Tuple[np.ndarray, float], ciphertext2: Tuple[np.ndarray, float], key: np.ndarray) -> bool:
    """同态比较运算（TLWE），返回True表示ciphertext1 > ciphertext2，False表示ciphertext1 <= ciphertext2"""
    # 计算差值
    negative_ciphertext2 = (-ciphertext2[0], -ciphertext2[1])
    diff_ciphertext = tfhe_float_add(ciphertext1, negative_ciphertext2)
    
    # 使用提供的密钥解密差值
    diff_plain = tfhe_tlwe.decrypt(diff_ciphertext, key)
    
    return diff_plain > 0

@app.route('/tfhe_compare_salaries', methods=['POST'])
def tfhe_compare_salaries():
    name1 = request.form.get('name1')
    name2 = request.form.get('name2')
    
    if not name1 or not name2:
        return jsonify({"error": "请提供两个员工姓名"}), 400
    
    if name1 not in tfhe_employees or name2 not in tfhe_employees:
        return jsonify({"error": "员工不存在"}), 400
    
    # 获取加密工资和对应的密钥
    employee1 = tfhe_employees[name1]
    employee2 = tfhe_employees[name2]
    
    # 使用正确的密钥进行同态比较
    result = tfhe_float_compare(
        employee1['ciphertext'], 
        employee2['ciphertext'],
        employee1['key']  # 使用第一个员工的密钥（两个密钥相同）
    )
    
    if result:
        return jsonify({"result": f"{name1}的工资低于{name2}"}), 200
    else:
        return jsonify({"result": f"{name1}的工资高于{name2}"}), 200

@app.route('/add_employee_tfhe', methods=['POST'])
def add_employee_tfhe():
    name = request.form.get('name')
    salary = float(request.form.get('salary'))
    
    if not name:
        return jsonify({"error": "请提供员工姓名"}), 400
    
    # 生成密钥
    key = tfhe_tlwe.keygen()
    
    # 加密工资
    ciphertext = tfhe_tlwe.encrypt(salary, key, tfhe_params.sigma)
    
    # 保存加密数据和密钥（实际应用中应安全存储）
    tfhe_employees[name] = {
        'ciphertext': ciphertext,
        'key': key
    }
    
    return jsonify({"message": f"员工{name}的工资（TFHE）已加密并保存", "name": name}), 200

@app.route('/tfhe_get_employees', methods=['GET'])
def tfhe_get_employees():
    """获取所有TFHE加密员工列表"""
    return jsonify(list(tfhe_employees.keys()))

if __name__ == '__main__':
    app.run(debug=True)