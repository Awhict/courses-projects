# import tensorflow as tf
# from tensorflow.keras.models import load_model
# import numpy as np
# import cv2
# from PIL import Image

# # 步骤 1：加密
# # 将中文字符转换为 Unicode 编码值
# # 将 Unicode 编码值转换为字符串形式，并在前面补零，使其长度固定（如5位）
# # 将所有编码值拼接成一个字符串
# # def encrypt(text):
# #     encrypted_text = ''
# #     for char in text:
# #         unicode_val = ord(char)
# #         # 将unicode编码值转换为固定长度的字符串
# #         encrypted_text += str(unicode_val).zfill(5)
# #     return encrypted_text

# # text = "佛龛是延安二保小自然课教员李涯"
# # encrypted_text = encrypt(text)
# # print("Encrypted Text:", encrypted_text)


# # 步骤 2：识别
# # 使用训练好的MNIST模型进行识别
# model = load_model('./mnist_model.h5')

# def preprocess_image(image_path):
#     # 加载图像并转换为灰度图
#     image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     # 使用二值化将图像转换为黑白图像
#     _, thresh = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
#     return thresh

# def recognize_digits(image_path):
#     image = preprocess_image(image_path)
#     # 检测图像中的轮廓
#     contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     digit_images = []
#     for cnt in contours:
#         x, y, w, h = cv2.boundingRect(cnt)
#         if w > 5 and h > 5:  # 过滤掉噪声
#             digit_image = image[y:y+h, x:x+w]
#             digit_image = cv2.resize(digit_image, (28, 28), interpolation=cv2.INTER_AREA)
#             digit_image = digit_image / 255.0
#             digit_image = digit_image.reshape(1, 28, 28, 1)
#             digit_images.append((digit_image, x))
    
#     # 按照x坐标排序
#     digit_images.sort(key=lambda x: x[1])
#     recognized_digits = []
#     for digit_image, _ in digit_images:
#         prediction = model.predict(digit_image)
#         predicted_digit = np.argmax(prediction)
#         recognized_digits.append(predicted_digit)
    
#     return recognized_digits

# image_path = './handnum.jpg'
# recognized_digits = recognize_digits(image_path)

# # 将识别的结果转换为字符串
# recognized_digits_str = ''.join(map(str, recognized_digits))
# # recognized_digits_str = "203154085926159243102343320108204452356733258289823583825945215922644628079"
# print("Recognized Digits:", recognized_digits_str)


# # 步骤 3：解密
# # 将数字字符串按照固定长度（如5位）分割
# # 将每个分割出来的字符串转换为整数（即 Unicode 编码值）
# # 将每个 Unicode 编码值转换为对应的字符
# def decrypt(encrypted_text):
#     decrypted_text = ''
#     i = 0
#     while i < len(encrypted_text):
#         # 以每5个字符为一组，解码成一个unicode编码值
#         unicode_val = int(encrypted_text[i:i+5])
#         decrypted_text += chr(unicode_val)
#         i += 5
#     return decrypted_text

# decrypted_text = decrypt(recognized_digits_str)
# print("Decrypted Text:", decrypted_text)

