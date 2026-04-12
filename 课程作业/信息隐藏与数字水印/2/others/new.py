from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def get_msg(msg):
    return msg.zfill(8)

def generate(msg):  # 将信息转置为2进制。
    result = ''
    for i in msg:
        if isinstance(i, int):
            result += get_msg(bin(i)).replace('0b', '')
        else:
            result += get_msg(bin(ord(i)).replace('0b', ''))
    return result

img = Image.open('buptgray.bmp').convert('L')  # 读取灰度图像
tmp_msg = 'BUPTshahexiaoqu'
hide_msg = generate(tmp_msg)
width, height = img.size
length = len(hide_msg)
count = 0  # 将信息隐藏到其最低位。

for i in range(height):
    if count == length:
        break
    for j in range(width):
        if count == length:
            break
        pixel = img.getpixel((i, j))
        new_pixel = pixel - pixel % 2 + int(hide_msg[count])
        img.putpixel((i, j), new_pixel)
        count += 1
        if count == length:
            break

img.save('buptgraystego.bmp')

plt.subplot(121)
plt.imshow(mpimg.imread('buptgray.bmp'), cmap='gray'), plt.title('Original'), plt.axis('off')
plt.subplot(122)
plt.imshow(mpimg.imread('buptgraystego.bmp'), cmap='gray'), plt.title('Encoded'), plt.axis('off')
plt.show()
