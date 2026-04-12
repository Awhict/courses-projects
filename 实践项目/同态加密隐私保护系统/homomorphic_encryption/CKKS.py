import tenseal as ts
import base64
from pathlib import Path
import json
from datetime import datetime

class CKKSComparator:
    def __init__(self, context_path="context.tenseal"):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        self.context_path = Path(context_path)

        if self.context_path.exists():
            # 读取并检查 context 是否包含 secret_key
            with open(self.context_path, "rb") as f:
                context_bytes = f.read()
                self.context = ts.context_from(context_bytes)

            if not self.context.is_private():
                raise ValueError("加载的 context 不包含 secret_key，请删除 context.tenseal 并重新运行程序。")

        else:
            #  创建新的 context，带 secret_key
            self.context = ts.context(
                ts.SCHEME_TYPE.CKKS,
                poly_modulus_degree=8192,
                coeff_mod_bit_sizes=[60, 40, 40, 60],
            )
            self.context.global_scale = 2**40
            self.context.generate_galois_keys()
            self.context.generate_relin_keys()

            with open(self.context_path, "wb") as f:
                f.write(self.context.serialize(save_secret_key=True))  # 保存 secret_key

    def encrypt(self, plain_data: float) -> str:
        vec = ts.ckks_vector(self.context, [plain_data])
        return base64.b64encode(vec.serialize()).decode()

    def decrypt(self, ciphertext: str) -> float:
        data = base64.b64decode(ciphertext)
        vec = ts.lazy_ckks_vector_from(data)
        vec.link_context(self.context)
        return vec.decrypt()[0]

    def _serialize(self, encrypted_vec) -> str:
        return base64.b64encode(encrypted_vec.serialize()).decode()

    def _deserialize(self, data: str):
        raw = base64.b64decode(data)
        vec = ts.lazy_ckks_vector_from(raw)
        vec.link_context(self.context)
        return vec

    def save_encrypted_file(self, filename: str, value: float) -> dict:
        filepath = self.data_dir / f"{filename}.json"
        if filepath.exists():
            raise ValueError("文件已存在")

        encrypted = self.encrypt(value)
        data = {
            "filename": filename,
            "data": encrypted,
            "timestamp": datetime.now().isoformat()
        }

        with open(filepath, "w") as f:
            json.dump(data, f)
        return data

    def list_files(self) -> list:
        return [
            json.load(f.open())
            for f in self.data_dir.glob("*.json")
        ]

    def compare(self, file1: str, file2: str) -> str:
        with (self.data_dir / f"{file1}.json").open() as f:
            data1 = json.load(f)
        with (self.data_dir / f"{file2}.json").open() as f:
            data2 = json.load(f)

        enc_a = self._deserialize(data1["data"])
        enc_b = self._deserialize(data2["data"])

        encrypted_diff = enc_a - enc_b
        decrypted_diff = self.decrypt(self._serialize(encrypted_diff))

        if decrypted_diff > 1e-3:
            relation = ">"
        elif decrypted_diff < -1e-3:
            relation = "<"
        else:
            relation = "="

        diff_value = abs(decrypted_diff)
        return f"{data1['filename']} {relation} {data2['filename']}，相差 {diff_value:.2f}"
