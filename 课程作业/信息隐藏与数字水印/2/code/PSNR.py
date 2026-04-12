import math
import numpy as np
import cv2

def psnr(img1, img2):
    img1 = np.float64(img1)
    img2 = np.float64(img2)
    mse = np.mean((img1 / 1.0 - img2 / 1.0) ** 2)
    if mse < 1.0e-10:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

original = cv2.imread('bupt.bmp')
contrastR = cv2.imread('buptgraystegoR.bmp')
contrastG = cv2.imread('buptgraystegoG.bmp')
contrastB = cv2.imread('buptgraystegoB.bmp')

resR = psnr(original, contrastR)
resG = psnr(original, contrastG)
resB = psnr(original, contrastB)

print('\033[47m\033[30m')
print(f"红色通道嵌入秘密信息携密隐写图像的峰值信噪比是{resR:.2f}")
# print(f"绿色通道嵌入秘密信息携密隐写图像的峰值信噪比是{resG:.2f}")
# print(f"蓝色通道嵌入秘密信息携密隐写图像的峰值信噪比是{resB:.2f}")

