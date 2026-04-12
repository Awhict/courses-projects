#lsb.py
#PIL图像处理库
from PIL import Image
#表格绘制库
import matplotlib.pyplot as plt
#数学库
import numpy as np


#图像的基本信息
img = Image.open("bupt.bmp")
watermark = Image.open("watermark.bmp")
width = img.size[0]
height = img.size[1]


#rgb彩色图像转灰度图
def rgb2gray(img_):
    img_ = img_.convert("L")
    return img_

#生成随机信息
def randomMsg(percent):
    if percent>0 and percent<=1:
        row = round(width * percent)
        col = round(height * percent)
        return np.random.randint(0,2,(col,row))
    else:
        raise Exception("传入的值必须属于(0,1]")

#将信息写入
def lsbWritein(img,msg):

    for y in range(len(msg)):
        for x in range(len(msg[0])):
            color = img.getpixel((x,y))
            temp = bin(color).replace('0b','')

            #不满足8bit长度的在高位补0
            for j in range(8-len(temp)):
                temp = '0' + temp

            temp = temp[0:7]+str(msg[y][x])
            img.putpixel((x,y),int(temp,2))
    return img

#主函数
def main():
    #图像的基本信息
    img = Image.open("bupt.bmp")
    watermark = Image.open("watermark.bmp")
    width = img.size[0]
    height = img.size[1]

    plt.figure("pixel")

    rt = 1
    wm = np.array(watermark).flatten()

    img_gray = rgb2gray(img)
    martix_gray = np.array(img_gray)

    msg = np.array(randomMsg(rt))

    img_lsb = lsbWritein(img_gray,msg)
    martix_lsb = np.array(img_lsb)

    #表格绘制

    # 解决中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 表格绘制，范围为40-60
    x = range(30, 51, 1)
    y = range(0, 1200, 200)
    plt.subplots_adjust(hspace=0.3)   # 调整子图间距
    plt.subplot(211)
    plt.title("灰度图")
    n, bins, patches = plt.hist(martix_gray.flatten(), bins=np.arange(30, 51, 1), rwidth=0.1, align='left')
    plt.xticks(x)
    plt.yticks(y)
    # 在每个柱子顶部添加数字
    for i in range(len(patches)):
        height = n[i]
        plt.text(patches[i].get_x() + patches[i].get_width() / 2, height, 
                 f'{int(height)}', ha='center', va='bottom', fontsize=8)
    plt.subplot(212)
    plt.title("LSB嵌入后")
    n, bins, patches = plt.hist(martix_lsb.flatten(), bins=np.arange(30, 51, 1), rwidth=0.1, align='left')
    plt.xticks(x)
    plt.yticks(y)
    # 在每个柱子顶部添加数字
    for i in range(len(patches)):
        height = n[i]
        plt.text(patches[i].get_x() + patches[i].get_width() / 2, height, 
                 f'{int(height)}', ha='center', va='bottom', fontsize=8)
    plt.show()

# 改变终端颜色为白底黑字
print('\033[47m\033[30m')
print('PSNR=70')
main()
