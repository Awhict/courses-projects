from PIL import Image
import matplotlib.pyplot as plt

# 将彩色图转换为灰度图
img = Image.open('bupt.bmp')
img_gray = img.convert('L')
img_gray.save("buptgray.bmp")
img = Image.open('buptgray.bmp')
width, height = img.size

# 创建一个子图用于显示8幅图像
fig, axs = plt.subplots(1, 8, figsize=(16, 2))
# 提取每个位平面并将其显示在子图中
for i, ax in enumerate(axs):
    plane = Image.new('L', (width, height))
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            bit = (pixel >> i) & 1
            plane.putpixel((x, y), bit*255)
    ax.imshow(plane, cmap='gray')
    ax.axis('off')

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.suptitle("2022212387 程彦超")
# plt.show()
