def read_file(file):
    """接收文件名为参数，读取文件中的数据到字符串中，返回这个字符串"""
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()


def char_statistics(txt):
    """接受字符串为参数，统计字符串中大写字母、小写字母、数字、空白字符和其他字符的数量，
    并将五组数据形成列表返回"""
    upper = lower = digit = space = other = 0          # 将五组字符数初始化为0
    for i in range(len(txt)):                          # 遍历字符串进行统计
        if txt[i].isupper():
            upper += 1
        elif txt[i].islower():
            lower += 1
        elif txt[i].isdigit():
            digit += 1
        elif txt[i].isspace():
            space += 1
        else:
            other += 1
    char_sta = [upper, lower, digit, space, other]     # 将统计结果存入列表
    return char_sta                                    # 返回列表


def number_of_word_list(txt):
    """接收字符串为参数，用空格替换字符串中所有标点符号，根据空格将字符串切分为列表，
    返回列表中单词数量，返回值为整型"""
    text = ''                                  # 创建空串text
    for i in range(len(txt)):                  # 遍历传入的字符串txt
        if txt[i].isalpha():                   # 如果是字母
            text += txt[i]                     # 则将该字母加入text
        elif txt[i].isdigit():                 # 如果是数字
            text += txt[i]                     # 则将该数字加入text
        else:                                  # 如果不是字母和数字
            text += ' '                        # 则将空格加入text
    #print(text)
    text = list(text.strip(' ').split(' '))    # 将字符串按空格分割为列表并去除末尾的空格
    while text.count(''):                      # 判断列表中是否有空值
        text.remove('')                        # 若有则移除
    #print(text)
    return len(text)                           # 返回值为列表的大小


def key_offset(key_txt):
    """接收一个密钥字符串作为参数，计算凯撒密码的偏移值并返回该偏移值"""
    key = 0
    for i in range(len(key_txt)):    # 计算所有字符的ASCII值之和
        key += ord(key_txt[i])
    key %= 26                        # 对26取模得到偏移量
    return key                       # 返回偏移量


def caesar_encrypt(text, offset):
    """接收一个加密的字符串text和一个整数offset为参数并采用字母表和数字中后面第offset个字符
    代替当前字符的方法对字符串中的字母和数字进行替换，实现加密效果，返回值为加密的字符串。"""
    ciphertext = ''                                                   # 创建密文空串
    for i in range(len(text)):
        if text[i].islower():
            ciphertext += chr((ord(text[i]) - 97 + offset)%26 + 97)   # 加密小写字母
        elif text[i].isupper():
            ciphertext += chr((ord(text[i]) - 65 + offset)%26 + 65)   # 加密大写字母
        elif not text[i].isalpha():
            ciphertext += text[i]                                     # 其他字符不加密(包括数字)
    return ciphertext                                                 # 返回密文


if __name__ == '__main__':
    key = input()                                                              # 输入密钥单词
    filename = 'E:\\Project\\Python\\pythonProject\\class_4\\mayun.txt'        # 文件路径
    text = read_file(filename)                                                 # 读取文件得到文件内容，存入text
    #text = 'ABCD  cd  123  +'
    char_sta = char_statistics(text)                                           # 对text中的内容进行统计
    print(char_sta[0], char_sta[1], char_sta[2], char_sta[3], char_sta[4])
    words_counts = number_of_word_list(text)                                   # 统计text里的单词数
    print(f'共有{words_counts}单词')
    key = key_offset(key)                                                      # 得到偏移量
    print(key)
    print(caesar_encrypt(text, key))                                           # 输出密文
