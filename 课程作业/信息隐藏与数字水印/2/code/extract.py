from PIL import Image
import numpy as np

# 加载隐写图像
stego_image = Image.open("buptgraystego.bmp").convert("L")
width, height = stego_image.size
stego_pixels = np.array(stego_image)

# 提取LSB隐写信息
binary_message = ""
for i in range(height):
    for j in range(width):
        # 获取每个像素的最低有效位
        binary_message += str(stego_pixels[i, j] & 1)

# 将提取的二进制信息转换为文本信息
# 假设秘密信息长度已知，逐8位转为字符
extracted_bits = binary_message[:len("BUPTshahexiaoqu") * 8]  # 截取相应长度的二进制数据
secret_message = ''.join([chr(int(extracted_bits[i:i+8], 2)) for i in range(0, len(extracted_bits), 8)])

# 输出结果
print("提取隐藏的秘密信息二进制为：", extracted_bits)
print("提取隐藏的秘密信息为：", secret_message)
