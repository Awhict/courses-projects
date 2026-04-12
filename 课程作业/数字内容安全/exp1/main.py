from utils import *


'''
import imagehash
import cv2
import numpy as np
from PIL import Image #PIL 是 python 的图像处理库

path1 = '1.jpg' 
path2 = '2.jpg' 

# ahash 算法
ahash1 = imagehash.average_hash(Image.open(path1))
ahash2 = imagehash.average_hash(Image.open(path2))
print(ahash1- ahash2)

# phash 算法
phash1 = imagehash.phash(Image.open(path1))
phash2 = imagehash.phash(Image.open(path2))
print(phash1- phash2)

# dhash 算法
dhash1 = imagehash.dhash(Image.open(path1))
dhash2 = imagehash.dhash(Image.open(path2))
print(dhash1- dhash2)

#whash 算法
whash1=imagehash.whash(Image.open(path1))
whash2=imagehash.whash(Image.open(path2))
print(whash1- whash2)
'''

# 输入选择的图像
a = input("请输入第一张图片的图片名：")
b = input("请输入第二张图片的图片名：")


# 读取两幅图像并进行预处理
image1 = preprocess_image(a)
image2 = preprocess_image(b)


# 显示预处理后的图像
# cv2.imshow("Image 1", image1)
# cv2.imshow("Image 2", image2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# 对标准化图像进行8*8子块划分和DCT变换
dct_image1 = block_dct(image1)
dct_image2 = block_dct(image2)


# 显示处理后的图像
# cv2.imshow("DCT Image 1", dct_image1)
# cv2.imshow("DCT Image 2", dct_image2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# 设置N值
N = 32
# 输入密钥
# key = eval(input("请输入纯数字密钥："))
key = 12345678
# 生成 N 个 64*64 伪随机矩阵
p_matrices = generate_pseudo_random_matrices(N, key)


# 显示第一个伪随机矩阵
# print("First Pseudo Random Matrix:")
# print(p_matrices[0])


# 得到一个周期延拓的DCT敏感度矩阵
M_matrix = sensitivity_matrix()


# 计算特征值权重
# weighted_Ic1 = dct_image1 * M_matrix
# weighted_Ic2 = dct_image2 * M_matrix
# 打印特征值权重矩阵
# print("weighted matrix:")
# print(weighted_Ic1)
# print(weighted_Ic2)


# 生成Hash向量
hash_vector1 = generate_hash_vectors(dct_image1, p_matrices, M_matrix)
hash_vector2 = generate_hash_vectors(dct_image2, p_matrices, M_matrix)


# 打印Hash向量
# print("Hash向量:", hash_vector1)
# print("Hash向量:", hash_vector1)


# 计算汉明距离
hamming_dis = hamming_distance(hash_vector1, hash_vector2)

# 设置tau值
tau = 5
# 打印阈值
# print("阈值:", float(tau/N))

# 打印汉明距离
# print("汉明距离为:", hamming_dis)
# print("汉明距离为:", float(hamming_dis/N))

# 打印判定结果
if hamming_dis < tau:
    print("两幅图像内容相同")
else:
    print("两幅图像内容不同")
