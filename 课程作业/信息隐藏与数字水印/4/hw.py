from PIL import Image
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare

def embed_message(image_path, output_path, message):
    # 打开灰度图像
    gray_image = Image.open(image_path).convert('L')  # 确保是灰度图像
    pixels = gray_image.load()

    # 获取图像的宽度和高度
    width, height = gray_image.size

    # 将消息转换为二进制形式
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # 嵌入信息
    index = 0
    for y in range(height):
        for x in range(width):
            if index < len(binary_message):
                # 获取当前像素的灰度值
                pixel_value = pixels[x, y]

                # 将 LSB 替换为二进制信息中的对应位
                new_pixel_value = (pixel_value & ~1) | int(binary_message[index])

                # 更新像素值
                pixels[x, y] = new_pixel_value

                # 移动到下一个二进制位
                index += 1
            else:
                # 如果信息已经嵌入完毕，剩余的像素点用随机数填充
                pixel_value = pixels[x, y]
                pixels[x, y] = (pixel_value & ~1) | random.randint(0, 1)

    # 保存嵌入信息后的图像
    gray_image.save(output_path)

def display_images(gray_image_path, stego_image_path):
    # 打开灰度图像和携密图像
    gray_image = Image.open(gray_image_path)
    stego_image = Image.open(stego_image_path)

    # 设置显示属性
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 创建子图
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # 显示灰度图像并添加标注
    axes[0].imshow(gray_image, cmap='gray')
    axes[0].set_title("2022212387-程彦超-原始灰度图")
    axes[0].axis('off')  # 关闭坐标轴

    # 显示携密图像并添加标注
    axes[1].imshow(stego_image, cmap='gray')
    axes[1].set_title("2022212387-程彦超-携密灰度图")
    axes[1].axis('off')  # 关闭坐标轴

    # 调整布局
    plt.tight_layout()

    # 显示图像
    plt.show()

def plot_histograms(original_image_path, stego_image_path):
    # 打开原始图像和携密图像
    original_image = Image.open(original_image_path)
    stego_image = Image.open(stego_image_path)

    # 获取图像的像素值
    original_pixels = np.array(original_image).flatten()
    stego_pixels = np.array(stego_image).flatten()

    # 设置显示属性
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 创建子图
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # 绘制原始图像的直方图
    axes[0].hist(original_pixels, bins=256, range=(0, 256), color='black', alpha=0.75)
    axes[0].set_title("2022212387-程彦超-原始图直方图")
    axes[0].set_xlabel("像素值")
    axes[0].set_ylabel("频数")

    # 绘制携密图像的直方图
    axes[1].hist(stego_pixels, bins=256, range=(0, 256), color='black', alpha=0.75)
    axes[1].set_title("2022212387-程彦超-LSB嵌入后直方图")
    axes[1].set_xlabel("像素值")
    axes[1].set_ylabel("频数")

    # 调整布局
    plt.tight_layout()

    # 保存直方图
    plt.savefig('histograms.png')

    # 显示直方图
    plt.show()

def chi_square_test(stego_image_path):
    # 打开携密图像
    stego_image = Image.open(stego_image_path)
    pixels = np.array(stego_image).flatten()

    # 统计像素值的频数
    observed_freq, _ = np.histogram(pixels, bins=256, range=(0, 256))

    # 计算期望频数（假设没有嵌入信息）
    expected_freq = (observed_freq[::2] + observed_freq[1::2]) / 2

    # 卡方检验
    chi2, p = chisquare(observed_freq[::2], f_exp=expected_freq)

    # 打印结果
    print(f"卡方值: {chi2:.2f}, p值: {p:.2f}")

    # 显示结果并添加标注
    plt.figure(figsize=(6, 4))
    plt.text(0.1, 0.5, f"2022212387程彦超\n卡方值: {chi2:.2f}\np值: {p:.2f}", fontsize=12)
    plt.axis('off')
    plt.savefig('chi_square_result.png')
    plt.show()

def main():
    # 输入图像路径
    input_image_path = 'bupt.bmp'
    gray_image_path = 'buptgray.bmp'
    stego_image_path = 'buptgraystego.bmp'

    # 要嵌入的消息
    message = "bupt"

    # 将彩色图像转换为灰度图像
    color_image = Image.open(input_image_path)
    gray_image = color_image.convert('L')
    gray_image.save(gray_image_path)

    # 使用 LSB 方法嵌入消息
    embed_message(gray_image_path, stego_image_path, message)

    print(f"灰度图像已保存为: {gray_image_path}")
    print(f"嵌入消息后的图像已保存为: {stego_image_path}")

    # 在一行两列中显示图像并添加标注
    display_images(gray_image_path, stego_image_path)

    # 绘制直方图
    plot_histograms(gray_image_path, stego_image_path)

    # 卡方分析
    # chi_square_test(stego_image_path)


if __name__ == "__main__":
    main()