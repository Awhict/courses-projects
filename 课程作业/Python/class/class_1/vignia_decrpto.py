print('本程序的功能为破解维吉尼亚密码')
print('请确定该程序的文件目录下有.txt 的文件用来存放使用维吉尼亚密码加密过的英文')
# 从文件中读取密文串 Cipher
CipherFile = open('E:\Project\Python\pythonProject\cipher_test.txt', 'r')
Cipher = CipherFile.read()
print('利用 Kasiski 测试法确定密钥长度')
# 寻找重复三字密文段
rst = []
for i in range(len(Cipher) - 2):
    a = Cipher.count(Cipher[i] + Cipher[i + 1] + Cipher[i + 2])
    if a >= 3:
        rst.append(Cipher[i] + Cipher[i + 1] + Cipher[i + 2])
# 格式化找到的重复三字密文段
rst = list(set(rst))
for letter in rst:
    for i in range(len(Cipher) - 2):
        if Cipher[i] + Cipher[i + 1] + Cipher[i + 2] == letter:
            print(i, letter)
print('利用重合指数法确定密钥具体内容')
CipherLen = int(input('请输入您根据 Kasiski 测试法确定的密钥长度：'))
# 建立使用相同密钥加密的字符串 Y
Y = [[] for i in range(CipherLen)]
for i in range(CipherLen):
    m = 0
    while m * CipherLen + i < len(Cipher):
        Y[i].append(Cipher[m * CipherLen + i])
        m = m + 1
# 建立字母表 alphabet
alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
# 计算重合指数 I_c
I_c = []
for i in range(CipherLen):
    p = 0
    for letter in alphabet:
        p += ((Y[i].count(letter) * (Y[i].count(letter) - 1)) / ((len(Y[i])) * (len(Y[i]) - 1)))
    I_c.append(p)
print('六个子密文串的重合指数分别为：\n', I_c)
print('六个子密文串的重合指数的平均值为：\n', sum(I_c) / CipherLen)
# 建立自然语言下 26 个英文字母出现频率表 p
p = [0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020, 0.061, 0.07, 0.002, 0.008, 0.04, 0.024, 0.067, 0.075, 0.019, 0.001, 0.06, 0.063, 0.091, 0.028, 0.01, 0.023, 0.001, 0.02, 0.001]
# 遍历 26 个英文字母，求对应的条件重合指数，找出具体密钥
for i in range(CipherLen):
    for g in range(26):
        M_g = 0
        for letter in alphabet:
            M_g += p[ord(letter) - 65] * Y[i].count(chr((ord(letter) - 65 + g) % 26 + 65)) * CipherLen / len(Cipher)
        print('第', i + 1, '位若为', chr(g + 65), '，条件重合指数为：', M_g)