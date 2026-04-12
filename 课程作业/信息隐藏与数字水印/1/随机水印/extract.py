# 导入wave音频文件处理库
import wave
# 导入数学计算库
import numpy as np

# 读取携密音频
wav = wave.open('embedded.wav', 'rb')
nchannels, sampwidth, framerate, nframes, comptype, compname = wav.getparams()
time = nframes / framerate

# 以字节方式读取携密音频的数据
frames = wav.readframes(nframes)

# 将字节数据转换为numpy数组
data = np.frombuffer(frames, dtype=np.uint8)

# LSB提取水印，提取前80比特
wm = np.zeros(80, dtype=np.uint8)
for i in range(len(wm)):
    wm[i] = data[i] % 2

print(f'Random Array: {wm}')
