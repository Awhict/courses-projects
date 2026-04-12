# 统计文件中的单词数量
def read_file(file):
    """接收文件名为参数，读取文件中的数据到字符串中，返回这个字符串"""
    with open(file, 'r', encoding='utf-8') as text:  # 创建文件对象
        txt =text.read()                             # 读文件为字符串
    return txt                                       # 返回字符串


def word_list(txt):
    """接收字符串为参数，用空格替换字符串中所有标点符号，根据空格将字符串切分为列表，返回值为元素是单词的列表"""
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
    return text                                # 返回列表


def number_of_words(ls):
    """接收一个以单词为元素的列表为参数，返回列表中单词数量，返回值为整型"""
    return len(ls)


if __name__ == '__main__':
    filename = input("请输入文件名:")              # 读入文件名
    text = read_file(filename)                    # 读取文件得到文件内容，存入text
    #text = 'a s d f.'
    words_list = word_list(text)                  # 处理text,得到单词的列表
    words_counts = number_of_words(words_list)    # 统计单词列表word_list里的单词数
    print(f'共有{words_counts}个单词')
