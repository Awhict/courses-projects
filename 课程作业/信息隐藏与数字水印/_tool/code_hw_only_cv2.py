import math
import numpy as np
import cv2
import matplotlib.pyplot as plt


def newline(func):
    def wrapper(*args, **kwargs):
        # print()
        ans = func(*args, **kwargs)
        print()
        return ans
    return wrapper


@newline
def step1():
    # 使用cv2读取图像
    img = cv2.imread("lena.bmp")
    

    # 设置显示属性
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
    # 创建一个新的图像窗口
    plt.figure(f"{student_id}+{name}")

    # 彩色图像
    plt.subplot(221)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 将BGR转换为RGB
    plt.imshow(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # 将RGB转换为BGR
    plt.title("彩色图像")
    plt.axis('off')

    # 红色通道
    plt.subplot(222)
    red_channel = img[:, :, 2]  # 提取红色通道
    plt.imshow(red_channel, cmap='Reds')
    plt.title(f"{student_id}+{name}+红色通道")
    plt.axis('off')

    # 绿色通道
    plt.subplot(223)
    green_channel = img[:, :, 1]  # 提取绿色通道
    plt.imshow(green_channel, cmap='Greens')
    plt.title(f"{student_id}+{name}+绿色通道")
    plt.axis('off')

    # 蓝色通道
    plt.subplot(224)
    blue_channel = img[:, :, 0]  # 提取蓝色通道
    plt.imshow(blue_channel, cmap='Blues')
    plt.title(f"{student_id}+{name}+蓝色通道")
    plt.axis('off')

    # 调整布局并保存显示的图像
    plt.tight_layout()
    plt.savefig(f"{student_id}+{name}.png", dpi=300)
    plt.show()


@newline
def step2():
    ascii_values = [ord(char) for char in message]
    binary_values = [format(ascii_val, '08b') for ascii_val in ascii_values]
    print(f'本人学号为{student_id}，本人的姓名为{name}，{message}的ASCII码转化为二进制的比特矩阵如下：')
    for binary_val in binary_values:
        print(binary_val)


@newline
def step3():
    # 读取图像
    img = cv2.imread("lena.bmp")

    # OpenCV使用BGR模式，因此蓝色通道是第0个通道
    b_channel = img[:, :, color_channel]

    # 获取第一行的len个像素点
    first_row_len = b_channel[0, 0:len] # 第0行的前len个像素点
    print(f"本人学号为{student_id}，本人姓名为{name}，{color_str}通道第一行从第1个像素点开始的len个像素点的十进制像素值矩阵如下：")
    # 打印8x8的区域，第1到第8个像素值输出在第一行，第9至16个像素值输出在第二行，17至24个像素值输出在第三行。依次类推
    for i in range(0, len, 8): # 这个range的意思是，从0开始，到len结束，步长为8，因此i会为0,8,16,24,32,40,48,56
        # 打印第i到第i+7个像素值
        print(' '.join(map(str, first_row_len[i:i+8])))

    # # 输出成二进制，可以用来debug
    # for i in range(0, len, 8):
    #     print(' '.join(map(lambda x: format(x, '08b'), first_row_len[i:i+8])))
    

@newline
def step4():
    def get_msg(msg):
        return msg.zfill(8)

    def generate(msg):  # 将信息转置为2进制。
        result = ''
        for i in msg:
            result += get_msg(bin(ord(i)).replace('0b', ''))
        return result

    # 使用cv2读取图像并提取蓝色通道
    img = cv2.imread("lena.bmp")
    blue_channel = img[:, :, color_channel]
    hide_msg = generate(message)

    # 将信息隐藏到蓝色通道最上面一行的len个像素点
    for i in range(len):
        pixel_value = blue_channel[0, i]
        pixel_value = pixel_value - pixel_value % 2 + int(hide_msg[i])
        blue_channel[0, i] = pixel_value

    # 输出嵌入后的蓝色通道最上面一行的len个像素点
    print(f"本人学号为{student_id}，本人姓名为{name}，{color_str}通道隐藏秘密信息后第一行从第1个像素点开始的len个像素点十进制像素值矩阵如下：")
    for i in range(0, len, 8):
        print(' '.join(map(str, blue_channel[0, i:i+8])))

    # # 二进制版，可以用来debug
    # for i in range(0, len, 8):
    #     print(' '.join(map(lambda x: format(x, '08b'), blue_channel[0, i:i+8])))
    
    # 保存修改后的图像
    cv2.imwrite('encode_lena.bmp', img)


@newline
def step5():
    # 读取原始图像和携密图像
    original_img = cv2.imread("lena.bmp")
    encoded_img = cv2.imread("encode_lena.bmp")

    # 因为OpenCV默认是BGR，所以我们转换它为RGB以使用matplotlib来显示
    original_img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    encoded_img_rgb = cv2.cvtColor(encoded_img, cv2.COLOR_BGR2RGB)

    # 设置显示属性
    plt.figure("原始图和携密图像对比")

    # 原始图像
    plt.subplot(1, 2, 1)  # 1行2列的第1个位置
    plt.imshow(original_img_rgb)
    plt.title(f"{student_id}+{name}+原始图像")
    plt.axis('off')

    # 携密图像
    plt.subplot(1, 2, 2)  # 1行2列的第2个位置
    plt.imshow(encoded_img_rgb)
    plt.title(f"{student_id}+{name}+携密图像")
    plt.axis('off')
    plt.suptitle(f"原始图和携密图像对比")

    plt.tight_layout()
    plt.savefig("原始图和携密图像.png", dpi=300)
    plt.show()

def psnr(img1, img2):
    img1 = np.float64(img1)
    img2 = np.float64(img2)
    mse = np.mean((img1 / 1.0 - img2 / 1.0) ** 2)
    if mse < 1.0e-10:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))


@newline
def step6():
    # 读取原始图像和携密图像
    original = cv2.imread("lena.bmp")
    contrast = cv2.imread("encode_lena.bmp")
    res = psnr(original, contrast)
    print(f"本人学号为{student_id}，本人的姓名为{name}，本人计算出来的PSNR的值为{res:.2f}")  # 输出小数位为2的浮点数


@newline
def step7():
    # 读取携密图像
    img = cv2.imread("encode_lena.bmp")

    # 获取蓝色通道
    b_channel = img[:, :, color_channel]

    # 将所有像素点的蓝色通道的最后一位置为1
    rows, cols = b_channel.shape
    for i in range(rows):
        for j in range(cols):
            if b_channel[i, j] % 2 == 0:
                b_channel[i, j] += 1  # 如果是偶数那就意味着最后一位是0，就给他加1变成1
    # 替换原始图像的蓝色通道为新的蓝色通道
    img[:, :, color_channel] = b_channel

    # 保存攻击后的图像
    cv2.imwrite("BlueStgeo1.bmp", img)

    # 读取攻击后的图像
    attacked_img = cv2.imread("BlueStgeo1.bmp")
    # cv2默认是BGR,因此这里的0对应蓝色通道
    attacked_img_blue = attacked_img[:, :, color_channel]
    # 读取未攻击的图像
    original_img = cv2.imread("encode_lena.bmp")
    original_img_blue = original_img[:, :, color_channel]

    # 比较第一行的len个像素点的蓝色通道的最低位
    changed_positions = []
    for i in range(len):
        original_pixel = original_img_blue[0, i] % 2
        attacked_pixel = attacked_img_blue[0, i] % 2
        if original_pixel != attacked_pixel:
            changed_positions.append(i)

    # 输出发生变化的像素位置
    print(f"本人学号为{student_id},本人姓名为{name}，攻击图像最第一行的len个点变化的位置如下：")
    for integer in changed_positions:
        print(integer, end=' ')

student_id = "2021212053"
name = "张原赫"
# 隐写信息为
message = "BUPTSCSS" # BUPTSCSS
# 需要隐藏的位为message * 8
len = len(message) * 8
color = "red" # blue or red or green
if color == "blue":
    color_channel = 0
    color_str = "蓝色"
elif color == "green":
    color_channel = 1
    color_str = "绿色"
elif color == "red":
    color_channel = 2
    color_str = "红色"
    
step1()
step2()
step3()
step4()
step5()
step6()
step7()
