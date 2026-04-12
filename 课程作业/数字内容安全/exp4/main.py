import numpy as np
import cv2
from scipy.fft import fft2, ifft2
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
from glob import glob
import random


# 读取图像并预处理
def preprocess_image(image_path, img_size=128):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(gray_image, (img_size, img_size))
    return resized_image


# 对图像进行离散傅立叶变换
def dft_image(image):
    return fft2(image)


# 计算拉普拉斯噪声
def laplace_noise(scale, size):
    return np.random.laplace(0, scale, size)


# 添加噪声到DFT系数中
def add_noise_to_dft(dft_matrix, epsilon, k):
    n, m = dft_matrix.shape
    selected_dft = dft_matrix[:k, :k]
    sensitivity = np.max(np.abs(selected_dft))
    lambda_ = sensitivity / epsilon
    noise = laplace_noise(lambda_, selected_dft.shape)
    dft_matrix[:k, :k] += noise
    return dft_matrix


# 逆DFT转换回图像
def idft_image(dft_matrix):
    return np.abs(ifft2(dft_matrix))


# PCA+SVM 人脸识别
def pca_svm_face_recognition(X_train, y_train, X_test, y_test, n_components=100):
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    pca = PCA(n_components=n_components)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)

    svm = SVC(kernel='linear', C=1)
    svm.fit(X_train_pca, y_train)
    y_pred = svm.predict(X_test_pca)

    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


# 主程序
def main(data_dir, epsilon=1.0, k=20, img_size=128):
    image_paths = glob(os.path.join(data_dir, '*.jpg'))
    # image_paths = glob(os.path.join(data_dir, '**', '*.jpg'), recursive=True)
    random.shuffle(image_paths)
    
    images = [preprocess_image(path, img_size) for path in image_paths]
    labels = [path.split('/')[-1].split('_')[0] for path in image_paths]    # 假设文件名格式为 'label_xxx.jpg'
    
    X = []
    for image in images:
        dft_matrix = dft_image(image)
        noisy_dft_matrix = add_noise_to_dft(dft_matrix, epsilon, k)
        noisy_image = idft_image(noisy_dft_matrix)
        X.append(noisy_image.flatten())

    X = np.array(X)
    y = np.array(labels)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    accuracy = pca_svm_face_recognition(X_train, y_train, X_test, y_test)
    print(f'差分隐私保护下的人脸识别准确率为: {accuracy:.4f}')


if __name__ == '__main__':
    data_dir = './lfw'  # LFW图像数据集的路径
    epsilon = 1.0
    k = 20
    main(data_dir, epsilon, k)
