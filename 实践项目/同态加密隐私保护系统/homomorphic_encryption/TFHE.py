import numpy as np
from typing import List, Tuple, Optional
import json
import traceback


class TFHEParameters:
    """TFHE加密方案的参数类"""

    def __init__(self, n: int, N: int, k: int, l: int, Bgbit: int, Bg: int,
                 sigma: float, sigma_min: float, h: int):
        self.n = n              # TLWE维度
        self.N = N              # 多项式阶数
        self.k = k              # TRLWE维度
        self.l = l              # TRGSW分解级别数
        self.Bgbit = Bgbit      # 每个分解级别的位数
        self.Bg = Bg            # 分解基数 (2^Bgbit)
        self.sigma = sigma      # 初始噪声标准差
        self.sigma_min = sigma_min  # 自举后的最小噪声标准差
        self.h = h              # 密钥的汉明重量


class Torus:
    """环面运算类，使用[-0.5, 0.5)表示"""

    @staticmethod
    def sample_uniform(size: int) -> np.ndarray:
        """在环面上均匀采样"""
        return np.random.uniform(-0.5, 0.5, size)

    @staticmethod
    def sample_gaussian(mean: float, sigma: float, size: int) -> np.ndarray:
        """在环面上高斯采样"""
        return np.mod(mean + np.random.normal(0, sigma, size), 1.0) - 0.5

    @staticmethod
    def add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """环面上的加法"""
        return np.mod(a + b, 1.0) - 0.5

    @staticmethod
    def multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """环面上的乘法（元素级）"""
        return np.mod(a * b, 1.0) - 0.5


class Polynomial:
    """多项式运算类，用于处理N次多项式"""

    def __init__(self, params: TFHEParameters):
        self.params = params

    def sample_random(self) -> np.ndarray:
        """生成随机多项式（系数为二进制）"""
        return np.random.randint(0, 2, self.params.N, dtype=np.int32)

    def sample_gaussian(self, sigma: float) -> np.ndarray:
        """生成高斯噪声多项式"""
        return Torus.sample_gaussian(0, sigma, self.params.N)

    def multiply(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """多项式乘法（在环R_q = Z[X]/(X^N+1)中）"""
        # 使用FFT加速多项式乘法
        a_fft = np.fft.rfft(a)
        b_fft = np.fft.rfft(b)
        result_fft = a_fft * b_fft
        result = np.fft.irfft(result_fft, self.params.N)
        return np.round(result).astype(np.int32)

    def add(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """多项式加法"""
        return (a + b) % 2

    def external_product(self, a: np.ndarray, b: List[np.ndarray]) -> np.ndarray:
        """多项式外积运算（加速版本）"""
        # 外积运算: a · b = a[0]*b[0] + a[1]*b[1] + ... + a[k]*b[k]
        result = np.zeros(self.params.N, dtype=np.float64)
        for i in range(len(a)):
            result = Torus.add(result, Torus.multiply(a[i], b[i]))
        return result


class FloatEncoder:
    """浮点数编码器，用于将浮点数编码为定点数"""

    def __init__(self, precision_bits: int = 30, max_value_bits: int = 14):
        """
        初始化浮点数编码器

        参数:
            precision_bits: 用于表示小数部分的位数
            max_value_bits: 用于表示整数部分的位数
        """
        self.precision_bits = precision_bits
        self.max_value_bits = max_value_bits
        self.scale = 1 << precision_bits  # 缩放因子：2^precision_bits
        self.max_int = (1 << (precision_bits + max_value_bits)) - 1  # 最大整数值
        self.min_int = -self.max_int      # 最小整数值

    def encode(self, value: float) -> int:
        """将浮点数编码为定点整数"""
        # 限制值的范围，防止溢出
        if value > self.max_value():
            value = self.max_value()
        if value < self.min_value():
            value = self.min_value()

        return int(round(value * self.scale))

    def decode(self, encoded: int) -> float:
        """将定点整数解码为浮点数"""
        # 处理有符号整数
        if encoded > (1 << (self.precision_bits + self.max_value_bits - 1)):
            encoded -= (1 << (self.precision_bits + self.max_value_bits))
        return encoded / self.scale

    def max_value(self) -> float:
        """可表示的最大浮点数"""
        return self.max_int / self.scale

    def min_value(self) -> float:
        """可表示的最小浮点数"""
        return self.min_int / self.scale


# 更新TLWE类以支持浮点数，改进环面解码
class TLWE:
    """TLWE加密结构"""

    def __init__(self, params: TFHEParameters, encoder: Optional[FloatEncoder] = None):
        self.params = params
        self.poly = Polynomial(params)
        self.encoder = encoder or FloatEncoder()  # 使用自定义编码器

    def keygen(self) -> np.ndarray:
        """生成TLWE密钥"""
        # 生成汉明重量为h的二进制密钥
        key = np.zeros(self.params.n, dtype=np.int32)
        indices = np.random.choice(self.params.n, self.params.h, replace=False)
        key[indices] = 1
        return key

    def encrypt(self, message: float, key: np.ndarray, sigma: float) -> Tuple[np.ndarray, float]:
        """加密浮点数到TLWE"""
        # 编码浮点数为定点整数
        encoded = self.encoder.encode(message)

        # 将定点整数转换为环面值 (-0.5, 0.5)
        # 调整缩放以适应环面表示
        torus_value = (encoded / (1 << 44)) - 0.5  # 使用更大的缩放因子

        a = np.random.randint(0, 2, self.params.n, dtype=np.int32)
        b = Torus.sample_gaussian(0, sigma, 1)[0]
        for i in range(self.params.n):
            b = Torus.add(b, Torus.multiply(a[i], key[i]))
        b = Torus.add(b, torus_value)
        return (a, b)

    def decrypt(self, ciphertext: Tuple[np.ndarray, float], key: np.ndarray) -> float:
        """从TLWE解密浮点数"""
        a, b = ciphertext
        mu = b
        for i in range(self.params.n):
            mu = Torus.add(mu, -Torus.multiply(a[i], key[i]))

        # 将环面值转换回定点整数
        torus_value = mu + 0.5  # 转换到 [0, 1) 范围
        encoded = int(round(torus_value * (1 << 44)))  # 使用相同的缩放因子

        # 使用改进的解码方法，处理有符号整数
        return self.encoder.decode(encoded)


# 更新TRLWE类以支持浮点数
class TRLWE:
    """TRLWE加密结构"""

    def __init__(self, params: TFHEParameters, encoder: Optional[FloatEncoder] = None):
        self.params = params
        self.poly = Polynomial(params)
        self.encoder = encoder or FloatEncoder()  # 使用自定义编码器

    def keygen(self) -> np.ndarray:
        """生成TRLWE密钥"""
        return self.poly.sample_random()

    def encrypt(self, message: float, key: np.ndarray, sigma: float) -> Tuple[np.ndarray, np.ndarray]:
        """加密浮点数到TRLWE"""
        if isinstance(message, np.ndarray):
            # 如果已经是多项式数组，直接使用
            message_poly = message
        else:
            # 编码浮点数为定点整数
            encoded = self.encoder.encode(message)

            # 创建多项式消息（只有常数项）
            message_poly = np.zeros(self.params.N, dtype=np.int32)
            message_poly[0] = encoded

        # 转换为环面值
        torus_poly = message_poly / (1 << 44) - 0.5  # 使用更大的缩放因子

        a = np.array([self.poly.sample_random() for _ in range(self.params.k)])
        b = self.poly.sample_gaussian(sigma)
        for i in range(self.params.k):
            b = self.poly.add(b, self.poly.multiply(a[i], key))
        b = self.poly.add(b, torus_poly)
        return (a, b)

    def decrypt(self, ciphertext: Tuple[np.ndarray, np.ndarray], key: np.ndarray) -> float:
        """从TRLWE解密浮点数"""
        a, b = ciphertext
        mu = b.copy()
        for i in range(self.params.k):
            mu = self.poly.add(mu, -self.poly.multiply(a[i], key))

        # 提取常数项
        torus_value = mu[0] + 0.5  # 转换到 [0, 1) 范围
        encoded = int(round(torus_value * (1 << 44)))  # 使用相同的缩放因子

        # 解码为浮点数
        return self.encoder.decode(encoded)


class TRGSW:
    """TRGSW加密结构"""

    def __init__(self, params: TFHEParameters):
        self.params = params
        self.poly = Polynomial(params)
        self.trlwe = TRLWE(params)

    def decompose(self, a: np.ndarray) -> List[np.ndarray]:
        """多项式分解操作"""
        result = []
        for j in range(self.params.l):
            temp = np.zeros(self.params.N, dtype=np.float64)
            for i in range(self.params.N):
                val = a[i]
                # 提取第j位的Bg进制表示
                digit = ((val >> (j * self.params.Bgbit)) & (self.params.Bg - 1)) / self.params.Bg
                temp[i] = digit
            result.append(temp)
        return result

    def keygen(self) -> np.ndarray:
        """生成TRGSW密钥"""
        return self.trlwe.keygen()

    def encrypt(self, message: np.ndarray, key: np.ndarray, sigma: float) -> List[List[Tuple[np.ndarray, np.ndarray]]]:
        """加密消息到TRGSW"""
        # TRGSW是一个2x(l*k)的TRLWE矩阵
        result = []
        for i in range(2):
            row = []
            for j in range(self.params.l * (self.params.k + 1)):
                # 对于每个位置，加密0或message
                msg = message if i == 1 else np.zeros(self.params.N, dtype=np.int32)
                row.append(self.trlwe.encrypt(msg, key, sigma))
            result.append(row)
        return result

    def external_product(self, trlwe: Tuple[np.ndarray, np.ndarray], trgsw: List[List[Tuple[np.ndarray, np.ndarray]]]) -> Tuple[np.ndarray, np.ndarray]:
        """TRGSW外积操作（加速版本）"""
        a, b = trlwe
        k = self.params.k

        # 初始化结果
        result_a = np.zeros((k, self.params.N), dtype=np.float64)
        result_b = np.zeros(self.params.N, dtype=np.float64)

        # 外积计算
        for j in range(self.params.l):
            for i in range(k + 1):
                if i < k:
                    # 处理a部分
                    coeff = a[i][j]
                    trlwe_part = trgsw[0][j*(k+1) + i]
                    for m in range(k):
                        result_a[m] = Torus.add(result_a[m], Torus.multiply(coeff, trlwe_part[0][m]))
                    result_b = Torus.add(result_b, Torus.multiply(coeff, trlwe_part[1]))
                else:
                    # 处理b部分
                    coeff = b[j]
                    trlwe_part = trgsw[1][j*(k+1) + i - k]
                    for m in range(k):
                        result_a[m] = Torus.add(result_a[m], Torus.multiply(coeff, trlwe_part[0][m]))
                    result_b = Torus.add(result_b, Torus.multiply(coeff, trlwe_part[1]))

        return (result_a, result_b)


# 更新Bootstrapping类，改进TRLWE自举处理
class Bootstrapping:
    """自举操作类"""

    def __init__(self, params: TFHEParameters):
        self.params = params
        self.tlwe = TLWE(params)
        self.trlwe = TRLWE(params)
        self.trgsw = TRGSW(params)
        self.poly = Polynomial(params)

    def keygen(self) -> Tuple[np.ndarray, np.ndarray, List[List[Tuple[np.ndarray, np.ndarray]]]]:
        """生成自举所需的全部密钥"""
        # 生成TLWE密钥
        tlwe_key = self.tlwe.keygen()

        # 生成TRLWE密钥（从TLWE密钥转换）
        trlwe_key = np.zeros(self.params.N, dtype=np.int32)
        trlwe_key[:self.params.n] = tlwe_key

        # 生成密钥切换密钥
        bk = self.generate_bootstrapping_key(tlwe_key, trlwe_key)

        return tlwe_key, trlwe_key, bk

    def generate_bootstrapping_key(self, tlwe_key: np.ndarray, trlwe_key: np.ndarray) -> List[List[Tuple[np.ndarray, np.ndarray]]]:
        """生成自举密钥（从TLWE到TRGSW的转换）"""
        # 为每个TLWE密钥位生成TRGSW加密
        bk = []
        for i in range(self.params.n):
            # 加密TRLWE密钥的第i位（使用TRGSW）
            message_poly = np.zeros(self.params.N, dtype=np.int32)
            message_poly[i] = self.tlwe.encoder.encode(1.0)

            encrypted = self.trgsw.encrypt(message_poly, trlwe_key, self.params.sigma)
            bk.append(encrypted)
        return bk

    def bootstrap_tlwe(self, ciphertext: Tuple[np.ndarray, float], bk: List[List[Tuple[np.ndarray, np.ndarray]]]) -> Tuple[np.ndarray, np.ndarray]:
        """执行自举操作，将TLWE转换为TRLWE并降低噪声"""
        a, b = ciphertext

        # 初始化结果
        result = np.zeros((self.params.k, self.params.N), dtype=np.float64)

        # 执行外积加速的自举
        for i in range(self.params.n):
            # 将TLWE的a[i]转换为多项式系数
            poly_coeff = np.zeros(self.params.N, dtype=np.float64)
            poly_coeff[0] = a[i]

            # 创建正确形状的TRLWE (k=2)
            # 修正：将poly_coeff扩展到k个维度
            trlwe_a = np.zeros((self.params.k, self.params.N), dtype=np.float64)
            trlwe_a[0] = poly_coeff  # 只填充第一个维度，其他维度保持为0

            trlwe_part = (trlwe_a, np.zeros(self.params.N, dtype=np.float64))

            # 使用密钥切换密钥和外积
            trgsw_part = bk[i]
            result_part = self.trgsw.external_product(trlwe_part, trgsw_part)

            # 累加结果
            for j in range(self.params.k):
                result[j] = Torus.add(result[j], result_part[0][j])

        # 处理b部分
        poly_coeff = np.zeros(self.params.N, dtype=np.float64)
        poly_coeff[0] = b

        # 创建正确形状的TRLWE
        trlwe_b = np.zeros((self.params.k, self.params.N), dtype=np.float64)
        trlwe_b[0] = poly_coeff

        # 返回自举后的TRLWE
        return (result, trlwe_b[0])

    def bootstrap_trlwe(self, ciphertext: Tuple[np.ndarray, np.ndarray], bk: List[List[Tuple[np.ndarray, np.ndarray]]]) -> Tuple[np.ndarray, np.ndarray]:
        """执行自举操作，处理TRLWE格式的密文"""
        a, b = ciphertext

        # 提取常数项（索引0位置）
        constant_term = b[0]

        # 创建一个新的TLWE密文，只包含常数项信息
        tlwe_ciphertext = (np.zeros(self.params.n), constant_term)

        # 使用TLWE自举函数
        trlwe_result = self.bootstrap_tlwe(tlwe_ciphertext, bk)

        # 确保返回正确格式的TRLWE
        return trlwe_result


# 添加浮点数的同态运算函数
def tfhe_float_add(ciphertext1: Tuple[np.ndarray, float], ciphertext2: Tuple[np.ndarray, float]) -> Tuple[np.ndarray, float]:
    """同态加法运算（TLWE）"""
    a1, b1 = ciphertext1
    a2, b2 = ciphertext2
    # 密文相加
    a_result = a1 + a2
    b_result = Torus.add(b1, b2)
    return (a_result, b_result)

# 同态比较函数
def tfhe_float_compare(ciphertext1: Tuple[np.ndarray, float], ciphertext2: Tuple[np.ndarray, float], tlwe: TLWE, key: np.ndarray) -> bool:
    """同态比较运算（TLWE），返回True表示ciphertext1 > ciphertext2，False表示ciphertext1 <= ciphertext2"""
    # 计算差值
    negative_ciphertext2 = (-ciphertext2[0], -ciphertext2[1])
    diff_ciphertext = tfhe_float_add(ciphertext1, negative_ciphertext2)

    # 解密差值
    diff = tlwe.decrypt(diff_ciphertext, key)

    return diff > 0


# 测试用例1：测试加法功能
def tfhe_example_1():
    # 定义参数（针对10000以内的数优化）
    params = TFHEParameters(
        n=1500,         # 增加TLWE维度提高安全性
        N=4096,         # 保持较高的多项式阶数
        k=4,            # 增加TRLWE维度
        l=6,            # 增加分解级别数
        Bgbit=12,       # 增加分解位数
        Bg=4096,        # 增加分解基数
        sigma=0.000001,  # 进一步减小初始噪声
        sigma_min=0.00000001, # 减小自举后的噪声
        h=30            # 增加密钥汉明重量
    )
    
    # 创建自定义编码器，增加精度和范围
    # 30位小数精度，14位整数范围，可以精确表示±16384以内的数
    encoder = FloatEncoder(precision_bits=30, max_value_bits=14)
    
    # 创建各类实例，使用自定义编码器
    torus = Torus()
    poly = Polynomial(params)
    tlwe = TLWE(params, encoder)
    trlwe = TRLWE(params, encoder)
    trgsw = TRGSW(params)
    boot = Bootstrapping(params)
    
    # 生成密钥
    tlwe_key, trlwe_key, bk = boot.keygen()
    
    # 定义测试用例，重点关注10000以内的数
    test_cases = [
        (2.5, 1.3),      # 基础正数
        (-2.1, 3.5),     # 负数与正数
        (-5.7, -2.3),    # 负数相加
        (0.0, 1.5),      # 零与正数
        (0.0, -0.9),     # 零与负数
        (1e-6, 1e-6),    # 极小正数
        (1000, 2000),    # 中等大小正数1
        (3000, 4000),    # 中等大小正数2
        (-1000, -2000),  # 中等大小负数1
        (-3000, -4000),  # 中等大小负数2
        (5000, 5000),    # 接近10000的数
        (9999.9, 0.1),   # 边界情况
        (-9999.9, -0.1), # 负边界情况
        (1e4, 1e4),      # 刚好超出范围
        (-1e4, -1e4),    # 负向超出范围
        (1e6, 1e6),      # 大数测试
        (-1e6, -1e6),    # 大负数测试
    ]
    
    for message1, message2 in test_cases:
        # 使用TLWE加密
        tlwe_ct1 = tlwe.encrypt(message1, tlwe_key, params.sigma)
        tlwe_ct2 = tlwe.encrypt(message2, tlwe_key, params.sigma)
        
        # 同态加法
        tlwe_sum = tfhe_float_add(tlwe_ct1, tlwe_ct2)
        
        # 解密结果
        decrypted_sum = tlwe.decrypt(tlwe_sum, tlwe_key)
        
        # 相对误差
        relative_error = abs((decrypted_sum - (message1 + message2)) / (message1 + message2)) * 100

        # 输出结果
        print(f"原始消息1: {message1}")
        print(f"原始消息2: {message2}")
        print(f"实际和: {message1 + message2}")
        print(f"同态和: {decrypted_sum}")
        print(f"相对误差: {abs(relative_error):.2f}%")

        print()


# 测试用例2：测试比较功能
def tfhe_example_2():
    # 定义参数（针对10000以内的数优化）
    params = TFHEParameters(
        n=1500,          # 增加TLWE维度提高安全性
        N=4096,         # 保持较高的多项式阶数
        k=4,            # 增加TRLWE维度
        l=6,            # 增加分解级别数
        Bgbit=12,       # 增加分解位数
        Bg=4096,        # 增加分解基数
        sigma=0.000001,  # 进一步减小初始噪声
        sigma_min=0.00000001, # 减小自举后的噪声
        h=30            # 增加密钥汉明重量
    )

    # 创建自定义编码器，增加精度和范围
    # 30位小数精度，14位整数范围，可以精确表示±16384以内的数
    encoder = FloatEncoder(precision_bits=30, max_value_bits=14)

    # 创建各类实例，使用自定义编码器
    torus = Torus()
    poly = Polynomial(params)
    tlwe = TLWE(params, encoder)
    trlwe = TRLWE(params, encoder)
    trgsw = TRGSW(params)
    boot = Bootstrapping(params)

    # 生成密钥
    tlwe_key, trlwe_key, bk = boot.keygen()

    # 定义测试用例，重点关注10000以内的数
    test_cases = [
        (2.5, 1.3),      # 基础正数
        (-2.1, 3.5),     # 负数与正数
        (-5.7, -2.3),    # 负数相加
        (0.0, 1.5),      # 零与正数
        (0.0, -0.9),     # 零与负数
        (1e-6, 1e-6),    # 极小正数
        (1000, 2000),    # 中等大小正数1
        (3000, 4000),    # 中等大小正数2
        (-1000, -2000),  # 中等大小负数1
        (-3000, -4000),  # 中等大小负数2
        (5000, 5000),    # 接近10000的数
        (9999.9, 0.1),   # 边界情况
        (-9999.9, -0.1), # 负边界情况
        (1e4, 1e4),      # 刚好超出范围
        (-1e4, -1e4),    # 负向超出范围
        (1e6, 1e6),      # 大数测试
        (-1e6, -1e6),    # 大负数测试
    ]

    for message1, message2 in test_cases:
        # 使用TLWE加密
        tlwe_ct1 = tlwe.encrypt(message1, tlwe_key, params.sigma)
        tlwe_ct2 = tlwe.encrypt(message2, tlwe_key, params.sigma)

        # 同态比较
        comparison_result = tfhe_float_compare(tlwe_ct1, tlwe_ct2, tlwe, tlwe_key)

        # 输出结果
        print(f"原始消息1: {message1}")
        print(f"原始消息2: {message2}")
        print(f"实际比较结果: {message1 > message2}")
        print(f"同态比较结果: {comparison_result}")
        print()


if __name__ == "__main__":
    # tfhe_example_1()
    tfhe_example_2()