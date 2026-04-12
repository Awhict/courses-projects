import tenseal as ts
from typing import Dict, Tuple
import json


class BFVCryptoSystem:
    def __init__(self, poly_modulus_degree=4096, plain_modulus=1032193):
        """
        初始化BFV加密系统

        参数:
            poly_modulus_degree: 多项式模数阶数，影响安全性和性能
            plain_modulus: 明文模数，决定能加密的整数范围
        """
        self.context = ts.context(
            ts.SCHEME_TYPE.BFV,
            poly_modulus_degree=poly_modulus_degree,
            plain_modulus=plain_modulus
        )
        self.encrypted_data: Dict[str, ts.BFVVector] = {}

    def generate_keys(self):
        """生成公私钥对"""
        self.context.generate_galois_keys()
        self.context.generate_relin_keys()
        return self.context

    def save_context(self, filename: str, secret_key=False):
        """
        保存加密上下文到文件

        参数:
            filename: 文件名
            secret_key: 是否保存私钥(默认False，出于安全考虑)
        """
        if secret_key:
            # 保存包含私钥的完整上下文
            with open(filename, 'wb') as f:
                f.write(self.context.serialize(save_secret_key=True))
        else:
            # 只保存公开参数和公钥
            with open(filename, 'wb') as f:
                f.write(self.context.serialize())

    def load_context(self, filename: str, secret_key=False):
        """
        从文件加载加密上下文

        参数:
            filename: 文件名
            secret_key: 是否加载私钥(默认False)
        """
        with open(filename, 'rb') as f:
            if secret_key:
                # 加载包含私钥的完整上下文
                self.context = ts.context_from(f.read())
            else:
                # 只加载公开参数和公钥
                self.context = ts.context_from(f.read())

    def encrypt(self, name: str, value: int):
        """
        加密数据并存储

        参数:
            name: 数据名称/标识符
            value: 要加密的整数值
        """
        if name in self.encrypted_data:
            raise ValueError(f"名称 '{name}' 已存在")

        encrypted_vector = ts.bfv_vector(self.context, [value])
        self.encrypted_data[name] = encrypted_vector
        return encrypted_vector

    def decrypt(self, name: str) -> int:
        """
        解密数据

        参数:
            name: 要解密的数据名称

        返回:
            解密后的整数值
        """
        if name not in self.encrypted_data:
            raise ValueError(f"名称 '{name}' 不存在")

        decrypted = self.encrypted_data[name].decrypt()
        return decrypted[0] if isinstance(decrypted, list) else decrypted

    def compare(self, name1: str, name2: str) -> Tuple[int, int]:
        """
        比较两个加密数据的大小并计算差值

        参数:
            name1: 第一个数据名称
            name2: 第二个数据名称

        返回:
            (比较结果, 差值)
            比较结果: 1表示name1>name2, -1表示name1<name2, 0表示相等
            差值: name1 - name2的加密差值
        """
        if name1 not in self.encrypted_data or name2 not in self.encrypted_data:
            raise ValueError("一个或两个名称不存在")

        # 计算差值
        diff = self.encrypted_data[name1] - self.encrypted_data[name2]

        # 解密差值来判断大小
        decrypted_diff = diff.decrypt()
        decrypted_diff = decrypted_diff[0] if isinstance(decrypted_diff, list) else decrypted_diff

        if decrypted_diff > 0:
            return 1, diff
        elif decrypted_diff < 0:
            return -1, diff
        else:
            return 0, diff

    def get_difference(self, name1: str, name2: str):
        """
        获取两个加密数据的差值(加密状态)

        参数:
            name1: 第一个数据名称
            name2: 第二个数据名称

        返回:
            加密的差值 (name1 - name2)
        """
        if name1 not in self.encrypted_data or name2 not in self.encrypted_data:
            raise ValueError("一个或两个名称不存在")

        return self.encrypted_data[name1] - self.encrypted_data[name2]

    def save_encrypted_data(self, filename: str):
        """保存加密数据到文件"""
        data_to_save = {}
        for name, encrypted_vec in self.encrypted_data.items():
            data_to_save[name] = encrypted_vec.serialize().hex()

        with open(filename, 'w') as f:
            json.dump(data_to_save, f)

    def load_encrypted_data(self, filename: str):
        """从文件加载加密数据"""
        with open(filename, 'r') as f:
            data_loaded = json.load(f)

        self.encrypted_data = {}
        for name, hex_data in data_loaded.items():
            self.encrypted_data[name] = ts.bfv_vector_from(
                self.context, bytes.fromhex(hex_data)
            )


# 示例用法
if __name__ == "__main__":
    # 创建加密系统
    bfv = BFVCryptoSystem()
    #bfv.generate_keys()

    # 加密数据
    bfv.encrypt("age1", 25)
    bfv.encrypt("age2", 30)
    bfv.encrypt("score1", 85)
    bfv.encrypt("score2", 85)

    # 解密数据
    print("解密 age1:", bfv.decrypt("age1"))
    print("解密 age2:", bfv.decrypt("age2"))

    # 比较大小
    result, diff = bfv.compare("age1", "age2")
    if result == 1:
        print("age1 > age2")
    elif result == -1:
        print("age1 < age2")
    else:
        print("age1 == age2")
    print("差值解密:", diff.decrypt()[0] if isinstance(diff.decrypt(), list) else diff.decrypt())

    # 另一个比较
    result, diff = bfv.compare("score1", "score2")
    if result == 1:
        print("score1 > score2")
    elif result == -1:
        print("score1 < score2")
    else:
        print("score1 == score2")
    print("差值解密:", diff.decrypt()[0] if isinstance(diff.decrypt(), list) else diff.decrypt())

    # 直接获取差值
    diff = bfv.get_difference("age2", "age1")
    print("age2 - age1 差值解密:", diff.decrypt()[0] if isinstance(diff.decrypt(), list) else diff.decrypt())

    # 保存和加载测试 - 这次保存私钥
    bfv.save_context("bfv_context.bin", secret_key=True)
    bfv.save_encrypted_data("encrypted_data.json")

    new_bfv = BFVCryptoSystem()
    new_bfv.load_context("bfv_context.bin", secret_key=True)
    new_bfv.load_encrypted_data("encrypted_data.json")
    print("加载后解密 age1:", new_bfv.decrypt("age1"))