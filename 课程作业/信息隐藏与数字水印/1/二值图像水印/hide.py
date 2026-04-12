# 导入wave音频文件处理库
import wave
# 导入图像处理库
import cv2
# 导入数学计算库
import numpy as np
# 导入绘图库
import matplotlib.pyplot as plt
# 导入随机数库
import random

# 读取载体音频
wav = wave.open('1.wav', 'rb')
nchannels, sampwidth, framerate, nframes, comptype, compname = wav.getparams()
time = nframes / framerate

# 以字节方式读取载体音频的数据
frames = wav.readframes(nframes)

# 以灰度图模式读取水印图像
wm = cv2.imread('bupt64.bmp', cv2.IMREAD_GRAYSCALE)

# 从二维矩阵转为一维并二值化
wm = wm.flatten() > 128
wm_length = len(wm)

wav_embedded = wave.open('1stego.wav', 'wb')
wav_embedded.setparams(wav.getparams())

# 将字节数据转换为numpy数组
data = np.frombuffer(frames, dtype=np.uint8)

# 设置密钥种子，生成伪随机序列
seed = 2022212387
random.seed(seed)
random_indices = random.sample(range(len(data)), wm_length)

# LSB嵌入水印
data_embedded = data.copy()
for i in range(wm_length):
    index = random_indices[i]
    data_embedded[index] -= data_embedded[index] % 2
    data_embedded[index] += wm[i]

# 写入音频数据
wav_embedded.writeframes(data_embedded)

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 展示原音频和嵌入音频的波形
plt.figure(figsize=(14, 6))
plt.xlabel("2022212387 程彦超")

plt.subplot(121)
plt.plot(data)
plt.title('原始音频')
plt.xticks([]), plt.yticks([])

plt.subplot(122)
plt.plot(data_embedded)
plt.title('嵌入音频')
plt.xticks([]), plt.yticks([])

plt.show()
