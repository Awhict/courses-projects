# 测试加密和解密

# 步骤 1：加密
# 将中文字符转换为 Unicode 编码值
# 将 Unicode 编码值转换为字符串形式，并在前面补零，使其长度固定（如5位）
# 将所有编码值拼接成一个字符串
def encrypt(text):
    encrypted_text = ''
    for char in text:
        unicode_val = ord(char)
        # 将unicode编码值转换为固定长度的字符串
        encrypted_text += str(unicode_val).zfill(5)
    return encrypted_text

text = "佛龛是延安二保小自然课教员李涯"
encrypted_text = encrypt(text)
print("Encrypted Text:", encrypted_text)
# Encrypted Text: 203154085926159243102343320108204452356733258289823583825945215922644628079

# 步骤 3：解密
# 将数字字符串按照固定长度（如5位）分割
# 将每个分割出来的字符串转换为整数（即 Unicode 编码值）
# 将每个 Unicode 编码值转换为对应的字符
def decrypt(encrypted_text):
    decrypted_text = ''
    i = 0
    while i < len(encrypted_text):
        # 以每5个字符为一组，解码成一个unicode编码值
        unicode_val = int(encrypted_text[i:i+5])
        decrypted_text += chr(unicode_val)
        i += 5
    return decrypted_text

decrypted_text = decrypt(encrypted_text)
print("Decrypted Text:", decrypted_text)
