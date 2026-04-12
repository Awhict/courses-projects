from PIL import Image
lena = Image.open("lena_std.bmp")
lena_gray = lena.convert('L')
lena_gray.show()
lena_gray.save("lena_gray.bmp")
