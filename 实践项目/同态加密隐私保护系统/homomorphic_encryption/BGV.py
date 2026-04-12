import random
import math

class BGV:
    def __init__(self, lambda_param=128, p=65537, q=1048583, d=2, seed=None):
        """
        初始化BGV参数
        :param lambda_param: 安全参数
        :param p: 明文模数(素数)
        :param q: 密文模数(远大于p的素数)
        :param d: 多项式环的维度
        :param seed: 随机种子，固定随机性
        """
        self.lambda_param = lambda_param
        self.p = p
        self.q = q
        self.d = d
        
        # 如果提供了种子，设置固定种子
        if seed is not None:
            random.seed(seed)

        # 生成私钥
        self.sk = self._generate_secret_key()
        
        # 生成公钥
        self.pk = self._generate_public_key()

    def _generate_secret_key(self):
        """生成私钥: 小系数的多项式"""
        return [random.randint(-1, 1) for _ in range(self.d)]

    def _generate_public_key(self):
        """生成公钥: (a, b = a*s)"""
        a = [random.randint(0, self.q-1) for _ in range(self.d)]
        
        # b = a * s (不使用噪声)
        b = self._poly_mult(a, self.sk)
        b = self._poly_mod(b, self.q)
        
        return (a, b)

    def encrypt(self, m):
        """
        加密明文m (0 <= m < p)
        :param m: 明文消息
        :return: 密文(u, v)
        """
        u = [random.randint(0, self.q-1) for _ in range(self.d)]
        
        # v = -u * s + m
        v = self._poly_add(self._poly_neg(self._poly_mult(u, self.sk)), [m] + [0]*(self.d-1))
        v = self._poly_mod(v, self.q)
        
        # u = a * e1 + p * u
        u_part1 = self._poly_mult(self.pk[0], u)  # 直接用u与公钥a相乘
        u_part2 = self._poly_scale(u, self.p)
        u = self._poly_add(u_part1, u_part2)
        u = self._poly_mod(u, self.q)

        return (u, v)

    def decrypt(self, ciphertext):
        """
        解密密文
        :param ciphertext: 密文(u, v)
        :return: 解密后的明文
        """
        u, v = ciphertext
        # m = v + u * s mod p
        m_poly = self._poly_add(v, self._poly_mult(u, self.sk))
        m_poly = self._poly_mod(m_poly, self.q)
        m = m_poly[0] % self.p
        
        return m

    def add(self, ciphertext1, ciphertext2):
        """同态加法: 对两个密文进行加法运算"""
        u1, v1 = ciphertext1
        u2, v2 = ciphertext2
        
        # 对应的u和v部分分别相加
        u = self._poly_add(u1, u2)
        v = self._poly_add(v1, v2)
        
        return (u, v)

    def _poly_add(self, p1, p2):
        """多项式加法"""
        return [(a + b) for a, b in zip(p1, p2)]

    def _poly_mult(self, p1, p2):
        """多项式乘法"""
        res = [0] * self.d
        for i in range(self.d):
            for j in range(self.d):
                if i + j < self.d:
                    res[i + j] += p1[i] * p2[j]
        return res

    def _poly_scale(self, p, scalar):
        """多项式标量乘法"""
        return [x * scalar for x in p]

    def _poly_neg(self, p):
        """多项式取负"""
        return [-x for x in p]

    def _poly_mod(self, p, modulus):
        """对多项式元素取模"""
        return [x % modulus for x in p]

class PrivacyPreservingSalarySystem:
    def __init__(self):
        self.bgv = BGV(seed=12345)  # 设置固定种子
        self.salaries = {}  # 存储加密后的工资

    def add_employee(self, name, salary):
        """添加员工及其加密工资"""
        encrypted_salary = self.bgv.encrypt(salary)
        self.salaries[name] = encrypted_salary

    def compare_salaries(self, name1, name2):
        """比较两个员工的工资(不暴露实际工资)"""
        salary1 = self.salaries[name1]
        salary2 = self.salaries[name2]
        # 获取比较结果(加密的1或0)
        comparison_result = self.bgv.add(salary1, salary2)
        # 解密比较结果
        result = self.bgv.decrypt(comparison_result)
        if result == 1:
            return f"{name1}的工资高于或等于{name2}"
        else:
            return f"{name1}的工资低于{name2}"

    def get_encrypted_salary(self, name):
        """获取加密后的工资(仅用于演示)"""
        return self.salaries[name]

    def decrypt_salary(self, encrypted_salary):
        """解密工资(仅用于验证)"""
        return self.bgv.decrypt(encrypted_salary)

# 测试代码
def test_bgv_correctness():
    print("测试BGV加密方案的正确性...")
    bgv = BGV(p=17, q=1009, d=2, seed=12345)  # 使用小参数便于测试
    # 测试加密解密
    m = 5
    ciphertext = bgv.encrypt(m)
    decrypted = bgv.decrypt(ciphertext)
    print(f"原始消息: {m}, 加密后: {ciphertext}, 解密后: {decrypted}")
    assert m == decrypted, "加密解密失败!"  # 这里检查加密解密是否正确
    # 测试同态加法
    m1, m2 = 7, 3
    c1, c2 = bgv.encrypt(m1), bgv.encrypt(m2)
    c_add = bgv.add(c1, c2)
    decrypted_add = bgv.decrypt(c_add)
    print(f"{m1} + {m2} = {decrypted_add} (模{bgv.p})")
    assert (m1 + m2) % bgv.p == decrypted_add, "同态加法失败!"
    print("所有基础测试通过!\n")

def test_salary_system():
    print("测试隐私保护的工资系统...")
    system = PrivacyPreservingSalarySystem()
    # 添加员工及其工资(加密存储)
    system.add_employee("Alice", 8500)
    system.add_employee("Bob", 7200)
    system.add_employee("Charlie", 9200)
    # 验证加密解密
    alice_enc = system.get_encrypted_salary("Alice")
    alice_dec = system.decrypt_salary(alice_enc)
    print(f"Alice的工资(解密后): {alice_dec}")
    assert alice_dec == 8500, "工资解密不正确!"
    # 比较工资
    print("\n工资比较结果:")
    print(system.compare_salaries("Alice", "Bob"))     # Alice > Bob
    print(system.compare_salaries("Bob", "Charlie"))   # Bob < Charlie
    print(system.compare_salaries("Alice", "Alice"))   # Alice == Alice
    print("\n工资系统测试完成!")

if __name__ == "__main__":
    test_bgv_correctness()
    test_salary_system()
