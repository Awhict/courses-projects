import cv2
import numpy as np
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'D:/Program Files/Tesseract-OCR/tesseract.exe'

# 图像预处理
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"无法加载图像: {image_path}")
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return image

# 识别数字
def recognize_digits(image_path):
    image = preprocess_image(image_path)
    # 使用Tesseract OCR进行数字识别
    custom_config = r'--oem 3 --psm 7 outputbase digits'
    recognized_digits_str = pytesseract.image_to_string(image, config=custom_config)
    return recognized_digits_str

# 解密
def decrypt(encrypted_text):
    decrypted_text = ''
    for i in range(0, len(encrypted_text), 5):
        if i+5 <= len(encrypted_text):
            unicode_val = int(encrypted_text[i:i+5])
            decrypted_text += chr(unicode_val)
    return decrypted_text

# 主函数
def main():
    image_path = './num.jpg'  # 输入图像路径
    try:
        recognized_digits_str = recognize_digits(image_path)
        recognized_digits_str = ''.join(filter(str.isdigit, recognized_digits_str))  # 过滤非数字字符
        print("Recognized Digits:", recognized_digits_str)
        # recognized_digits_str = "203154085926159243102343320108204452356733258289823583825945215922644628079"
        decrypted_text = decrypt(recognized_digits_str)
        print("Decrypted Text:", decrypted_text)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
