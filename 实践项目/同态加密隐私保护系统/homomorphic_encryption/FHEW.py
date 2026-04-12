import tenseal as ts
import ast
import os
import hashlib
import base64

CONTEXT_DIR = "contexts"
HASH_DIR = "contexts/hashes"
os.makedirs(CONTEXT_DIR, exist_ok=True)
os.makedirs(HASH_DIR, exist_ok=True)

CONTEXT_FILE = "context.tenseal"

class SEALBooleanEncryptor:
    def __init__(self):
        if os.path.exists(CONTEXT_FILE):
            with open(CONTEXT_FILE, "rb") as f:
                self.context = ts.context_from(f.read())
        else:
            self.context = ts.context(
                ts.SCHEME_TYPE.BFV,
                poly_modulus_degree=4096,
                plain_modulus=1032193
            )
            self.context.generate_galois_keys()
            self.context.generate_relin_keys()
            with open(CONTEXT_FILE, "wb") as f:
                f.write(self.context.serialize(save_secret_key=True))

    def _compute_hash(self, byte_data):
        return hashlib.sha256(byte_data).hexdigest()

    def _load_context_hash(self):
        if not os.path.exists(self.hash_file):
            return None
        with open(self.hash_file, "r") as f:
            return f.read().strip()

    def verify_context_compatibility(self, ciphertexts):
        """用于解密前检查当前 context 是否能解密密文"""
        try:
            _ = [c.decrypt()[0] for c in ciphertexts]
            return True
        except Exception as e:
            print(f"[上下文验证失败] 解密失败: {e}")
            return False

    def encrypt_bit(self, m):
        return ts.bfv_vector(self.context, [int(m)])

    def decrypt_bit(self, ciphertext):
        return round(ciphertext.decrypt()[0]) % 2

    def encrypt_integer(self, m):
        bits = list(map(int, bin(m)[2:].zfill(16)))
        return [self.encrypt_bit(b) for b in bits]

    def decrypt_integer(self, ciphertexts):
        bits = [self.decrypt_bit(c) for c in ciphertexts]
        return int("".join(map(str, bits)), 2)

    def force_bit(self, c):
        return c * c

    def homomorphic_not(self, c):
        return self.force_bit(self.encrypt_bit(1) - c)

    def homomorphic_and(self, c1, c2):
        return self.force_bit(c1 * c2)

    def homomorphic_or(self, c1, c2):
        return self.force_bit(c1 + c2 - c1 * c2)

    def homomorphic_xor(self, c1, c2):
        return self.force_bit(c1 + c2 - 2 * (c1 * c2))

    def homomorphic_nand(self, c1, c2):
        return self.homomorphic_not(self.homomorphic_and(c1, c2))

    def homomorphic_nor(self, c1, c2):
        return self.homomorphic_not(self.homomorphic_or(c1, c2))

    def homomorphic_xnor(self, c1, c2):
        return self.homomorphic_not(self.homomorphic_xor(c1, c2))

    def debug_decrypt_bits(self, ciphertexts):
        return [round(c.decrypt()[0], 2) for c in ciphertexts]

    def evaluate_expression(self, expr: str, inputs: dict):
        encrypted_inputs = {k: self.encrypt_bit(int(v)) for k, v in inputs.items()}

        def eval_ast(node):
            if isinstance(node, ast.Name):
                return encrypted_inputs[node.id]
            elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
                return self.homomorphic_not(eval_ast(node.operand))
            elif isinstance(node, ast.BoolOp):
                values = [eval_ast(v) for v in node.values]
                if isinstance(node.op, ast.And):
                    result = values[0]
                    for v in values[1:]:
                        result = self.homomorphic_and(result, v)
                    return result
                elif isinstance(node.op, ast.Or):
                    result = values[0]
                    for v in values[1:]:
                        result = self.homomorphic_or(result, v)
                    return result
            elif isinstance(node, ast.BinOp):
                left = eval_ast(node.left)
                right = eval_ast(node.right)
                if isinstance(node.op, ast.BitXor):
                    return self.homomorphic_xor(left, right)
                else:
                    raise ValueError(f"Unsupported binary op: {type(node.op)}")
            else:
                raise ValueError("Unsupported AST node")

        tree = ast.parse(expr, mode="eval")
        return eval_ast(tree.body)
