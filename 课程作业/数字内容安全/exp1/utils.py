import numpy as np


def preprocess_image(image_path):
    '''读入图像并对图像做预处理：
    如果读入的是彩色图像，将其转换为灰度图像；
    在灰度图像中利用差值方式将图像重采样为 64*64的标准化图表示'''
    import cv2
    # 读入图像
    image = cv2.imread(image_path)
    
    # 将彩色图像转换为灰度图像
    if len(image.shape) > 2:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image
    
    # 将图像重采样为 64*64
    resized_image = cv2.resize(gray_image, (64, 64))
    
    return resized_image


def dct2(block):
    '''对图像进行二维离散余弦变换'''
    from scipy.fftpack import dct
    return dct(dct(block.T, norm='ortho').T, norm='ortho')


def block_dct(image):
    '''对标准化图像进行8*8子块划分, 将标准化图像划分为64个子块, 并依次对各子块进行二维离散余弦变换。'''
    # 获取图像大小
    rows, cols = image.shape
    
    # 初始化结果矩阵
    result = np.zeros_like(image)
    
    # 定义块大小
    block_size = 8
    
    # 将图像划分为块，并对每个块进行DCT变换
    for r in range(0, rows, block_size):
        for c in range(0, cols, block_size):
            block = image[r:r+block_size, c:c+block_size]
            # 进行二维离散余弦变换
            dct_block = dct2(block)
            # 将每个块的DC系数置为0
            dct_block[0, 0] = 0
            result[r:r+block_size, c:c+block_size] = dct_block
    
    return result


def generate_pseudo_random_matrices(N, key):
    '''通过密钥key生成n个64*64的伪随机矩阵'''
    from scipy.ndimage import convolve
    # 设置随机种子
    np.random.seed(key)
    
    # 生成 N 个 64*64 服从标准正态分布的伪随机矩阵
    random_matrices = [np.random.randn(64, 64) for _ in range(N)]
    
    # 定义高斯低通滤波器
    gaussian_filter = np.array([[1, 4, 6, 4, 1],
                                 [4, 16, 24, 16, 4],
                                 [6, 24, 36, 24, 6],
                                 [4, 16, 24, 16, 4],
                                 [1, 4, 6, 4, 1]]) / 256.0
    
    # 对每个伪随机矩阵进行迭代滤波
    filtered_matrices = []
    for matrix in random_matrices:
        filtered_matrix = convolve(matrix, gaussian_filter, mode='constant', cval=0.0)
        filtered_matrices.append(filtered_matrix)
    
    return filtered_matrices


def sensitivity_matrix():
    '''得到一个周期延拓的DCT敏感度矩阵'''
    # 定义DCT敏感度矩阵m
    m = np.array([
        [71.43, 99.01, 86.21, 60.24, 41.67, 29.16, 20.88, 15.24],
        [99.01, 68.97, 75.76, 65.79, 50.00, 36.90, 27.25, 20.28],
        [86.21, 75.76, 44.64, 38.61, 33.56, 27.47, 21.74, 17.01],
        [60.24, 65.79, 38.61, 26.53, 21.98, 18.87, 15.92, 13.16],
        [41.67, 50.00, 33.56, 21.98, 16.26, 13.14, 11.48, 9.83],
        [29.16, 36.90, 27.47, 18.87, 13.14, 10.40, 8.64, 7.40],
        [20.88, 27.25, 21.74, 15.92, 11.48, 8.64, 6.90, 5.78],
        [15.24, 20.28, 17.01, 13.16, 9.83, 7.40, 5.78, 4.73]
    ])

    # 周期延拓得到大小为64×64的矩阵M
    M = np.tile(m, (8, 8))

    return M


def generate_hash_vectors(image_matrix, pseudo_random_matrices, sensitivity_matrix):
    '''计算得到hash向量'''
    hash_vector = ""
    for p_matrix in pseudo_random_matrices:
        hash_temp = 0
        for i in range(64):
            for j in range(64):
                hash_temp += image_matrix[i, j] * p_matrix[i, j] * sensitivity_matrix[i, j]
        if hash_temp < 0:
            hash_value = 0
        else:
            hash_value = 1
        hash_vector += str(hash_value)
    return hash_vector


def hamming_distance(hash_vector1, hash_vector2):
    '''计算两个hash向量的汉明距离'''
    if len(hash_vector1) != len(hash_vector2):
        raise ValueError("Hash向量的长度不相同")
    distance = 0
    for i in range(len(hash_vector1)):
        if hash_vector1[i] != hash_vector2[i]:
            distance += 1
    return distance
