# 导入wave音频文件处理库
import wave
# 导入数学计算库
import numpy as np
# 导入绘图库
import matplotlib.pyplot as plt

# 读取载体音频
wav = wave.open('carrier.wav', 'rb')
nchannels, sampwidth, framerate, nframes, comptype, compname = wav.getparams()
time = nframes / framerate

# 以字节方式读取载体音频的数据
frames = wav.readframes(nframes)

# 产生随机的80比特长的水印数据
wm_random = np.random.randint(0, 2, 80)
print(f'Random Array: {wm_random}')

wav_embedded = wave.open('embedded.wav', 'wb')
wav_embedded.setparams(wav.getparams())

# 将字节数据转换为numpy数组
data = np.frombuffer(frames, dtype=np.uint8)

# LSB嵌入水印
data_embedded = data.copy()
for i in range(len(wm_random)):
    data_embedded[i] -= data_embedded[i] % 2
    data_embedded[i] += wm_random[i]

# 写入音频数据
wav_embedded.writeframes(data_embedded)

# 展示原音频和嵌入音频的波形
plt.figure(figsize=(14, 6))

plt.subplot(121)
plt.plot(data)
plt.title('Original Audio')
plt.xticks([]), plt.yticks([])

plt.subplot(122)
plt.plot(data_embedded)
plt.title('Embedded Audio')
plt.xticks([]), plt.yticks([])

plt.show()
