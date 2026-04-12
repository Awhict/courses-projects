from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# 加载灰度图像
original_image = Image.open("buptgray.bmp").convert("L")
width, height = original_image.size
pixels = np.array(original_image)

# 将秘密信息编码为二进制
secret_message = "BUPTshahexiaoqu"
binary_message = ''.join([format(ord(c), '08b') for c in secret_message])
message_length = len(binary_message)

# 嵌入秘密信息
stego_pixels = pixels.copy()
msg_index = 0
for i in range(height):
    for j in range(width):
        if msg_index < message_length:
            # 取出当前像素的最低有效位并替换
            pixel_bin = format(stego_pixels[i, j], '08b')
            new_pixel_bin = pixel_bin[:-1] + binary_message[msg_index]
            stego_pixels[i, j] = int(new_pixel_bin, 2)
            msg_index += 1
        else:
            break

# 将隐写图像保存
stego_image = Image.fromarray(stego_pixels)
stego_image.save("buptgraystego.bmp")

# 显示原始和隐写图像
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].imshow(original_image, cmap='gray')
axs[0].set_title("原始图像")
axs[0].axis('off')

axs[1].imshow(stego_image, cmap='gray')
axs[1].set_title("携密图像")
axs[1].axis('off')

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.suptitle("2022212387 程彦超")
plt.show()
