import numpy as np
import cv2
import pywt
import matplotlib.pyplot as plt

# 1. 嵌入水印
def DWT_DCT_SVD(coverImage, watermarkImage):
    # Resize the cover image and watermark image
    coverImage = cv2.resize(coverImage, (512, 512))
    watermarkImage = cv2.resize(watermarkImage, (256, 256))
    
    # Convert to float32 for processing
    coverImage = np.float32(coverImage) / 255.0
    watermarkImage = np.float32(watermarkImage)
    
    # Perform DWT on the cover image
    coeff = pywt.dwt2(coverImage[:, :, 0], 'haar')  # Apply DWT only on the red channel
    cA, (cH, cV, cD) = coeff
    
    # Perform DCT on the watermark image
    watermarkImage_dct = cv2.dct(watermarkImage)
    
    # Perform SVD on the DCT of both cover image and watermark
    cA_dct = cv2.dct(cA)
    ua, sa, va = np.linalg.svd(cA_dct, full_matrices=1, compute_uv=1)
    uw, sw, vw = np.linalg.svd(watermarkImage_dct, full_matrices=1, compute_uv=1)
    
    # Embedding process
    alpha = 10  # Embedding strength
    sA = np.zeros((256, 256), np.uint8)
    sA[:256, :256] = np.diag(sa)
    sW = np.zeros((256, 256), np.uint8)
    sW[:256, :256] = np.diag(sw)
    W = sA + alpha * sW

    u1, w1, v1 = np.linalg.svd(W, full_matrices=1, compute_uv=1)
    ww = np.zeros((256, 256), np.uint8)
    ww[:256, :256] = np.diag(w1)
    Wmodi = np.matmul(ua, np.matmul(ww, va))

    # Inverse DCT and IDWT
    widct = cv2.idct(Wmodi)
    
    # Embed the modified DCT coefficients into the red channel
    watermarkedRedChannel = pywt.idwt2((widct, (cH, cV, cD)), 'haar')
    
    # Create the watermarked image by embedding in the red channel only
    watermarkedImage = coverImage.copy()
    watermarkedImage[:, :, 0] = watermarkedRedChannel  # Modify only the red channel
    
    # Convert back to 8-bit for displaying
    watermarkedImage = np.uint8(watermarkedImage * 255)

    # 保存嵌入水印后的图像
    # cv2.imwrite('buptstegoR.bmp', watermarkedImage)

    return watermarkedImage

# 2. 计算PSNR
def compute_psnr(original_image, stego_image):
    mse = np.mean((original_image - stego_image) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr

# 3. 提取水印
def extract_watermark(watermarkedImage, coverImage, alpha=10):
    # Resize images to 512x512
    watermarkedImage = cv2.resize(watermarkedImage, (512, 512))
    coverImage = cv2.resize(coverImage, (512, 512))

    # Convert to float32 for processing
    watermarkedImage = np.float32(watermarkedImage) / 255.0
    coverImage = np.float32(coverImage) / 255.0
    
    # Extract red channel from watermarked image and cover image
    watermarkedRedChannel = watermarkedImage[:, :, 0]
    coverRedChannel = coverImage[:, :, 0]

    # Perform DWT on both red channels (watermarked and cover image)
    coeff_cover = pywt.dwt2(coverRedChannel, 'haar')
    cA_cover, (cH_cover, cV_cover, cD_cover) = coeff_cover
    coeff_watermarked = pywt.dwt2(watermarkedRedChannel, 'haar')
    cA_watermarked, (cH_watermarked, cV_watermarked, cD_watermarked) = coeff_watermarked
    
    # Perform DCT on both cA components (cover and watermarked)
    cA_cover_dct = cv2.dct(cA_cover)
    cA_watermarked_dct = cv2.dct(cA_watermarked)

    # Perform SVD on both DCT components (cover and watermarked)
    ua_cover, sa_cover, va_cover = np.linalg.svd(cA_cover_dct, full_matrices=1, compute_uv=1)
    ua_watermarked, sa_watermarked, va_watermarked = np.linalg.svd(cA_watermarked_dct, full_matrices=1, compute_uv=1)

    # Extract watermark information from the SVD components
    sW = (sa_watermarked - sa_cover) / alpha  # Extract watermark information

    # Construct a diagonal matrix for watermark (as a 2D matrix)
    watermarkImage = np.zeros_like(cA_cover, np.float32)
    watermarkImage[:len(sW), :len(sW)] = np.diag(sW)  # Only store the diagonal values in the matrix
    
    # Perform inverse SVD on the extracted watermark
    W_dct_reconstructed = np.matmul(ua_watermarked, np.matmul(np.diag(sW), va_watermarked))
    
    # Perform inverse DCT to recover the watermark
    watermarkImage_reconstructed = cv2.idct(W_dct_reconstructed)
    
    # Thresholding to recover the binary watermark image
    watermarkImage_binary = (watermarkImage_reconstructed > 0).astype(np.uint8) * 255

    # 保存嵌入水印后的图像
    # cv2.imwrite('watermark1.bmp', watermarkImage_binary)

    return watermarkImage_binary

# 4. 计算NC
def NC(template, img):
    template = template.astype(np.uint8)
    img = img.astype(np.uint8)
    return cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)[0][0]

# 5. 高斯噪声攻击
def gaussian_attack(img, mean, sigma):
    img = img.astype(np.float32) / 255
    noise = np.random.normal(mean, sigma, img.shape)
    img_gaussian = img + noise
    img_gaussian = np.clip(img_gaussian, 0, 1)
    img_gaussian = np.uint8(img_gaussian * 255)
    return img_gaussian

# 水印嵌入
coverImage = cv2.imread('bupt.bmp') 
watermarkImage = cv2.imread('watermark.bmp', cv2.IMREAD_GRAYSCALE) 
watermarkedImage = DWT_DCT_SVD(coverImage, watermarkImage)
# cv2.imwrite('buptstegoR.bmp', watermarkedImage)

# 计算PSNR
stego_image = cv2.imread('buptstegoR.bmp')
psnr_value = compute_psnr(coverImage, stego_image)
print(f"PSNR: {psnr_value:.3f} dB")

# 对携密图像进行高斯噪声攻击，标准差设置为0.002
img_gaussian = gaussian_attack(stego_image, 0, 0.002)
cv2.imwrite('buptstegoR1.bmp', img_gaussian)

# 提取水印
# watermarkedImage = cv2.imread('buptstegoR.bmp') 
watermarkedImage = cv2.imread('buptstegoR1.bmp') 
coverImage = cv2.imread('bupt.bmp') 
extracted_watermark = extract_watermark(watermarkedImage, coverImage)
# cv2.imwrite('watermark1.bmp', extracted_watermark)
cv2.imwrite('watermark2.bmp', extracted_watermark)

# 计算NC
nc = NC(watermarkImage, extracted_watermark)
print('%s %.3f %s' % ('NC = ', nc * 100, '%'))

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 显示原图和嵌入水印后的图像
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB))
plt.title("2022212387+程彦超+原始图像")
plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(watermarkedImage, cv2.COLOR_BGR2RGB))
plt.title("2022212387+程彦超+嵌入图像")
plt.show()

# 显示原水印和受攻击后的水印
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(watermarkImage, cv2.COLOR_BGR2RGB))
plt.title("2022212387+程彦超+原始水印")
plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(extracted_watermark, cv2.COLOR_BGR2RGB))
plt.title("2022212387+程彦超+攻击后水印")
plt.show()
