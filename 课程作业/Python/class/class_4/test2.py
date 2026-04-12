#凯撒密码————加密
import string


def caesar_cipher(text):
    """接收一个字符串为参数，采用字母表和数字中后面第3个字符代替当前字符的方法
    对字符串中的字母和数字进行替换，实现加密效果，返回值为加密的字符串。
    例如：2019 abc 替换为5342 def """
    lowers = string.ascii_lowercase                      #lowers是全部的小写英文字母
    uppers = string.ascii_uppercase                      #uppers是全部的大写英文字母
    digits = string.digits                               #digits是全部的数字字符
    lowers_c = lowers[3:-1] + lowers[-1] + lowers[0:3]   #lowers_c是移位后的lowers
    uppers_c = uppers[3:-1] + uppers[-1] + uppers[0:3]   #uppers_c是移位后的uppers
    digits_c = digits[3:-1] + digits[-1] + digits[0:3]   #digits_c是移位后的digits
    plaintext = lowers + uppers + digits                 #明文表
    ciphertext = lowers_c + uppers_c + digits_c          #密文表
    table = ''.maketrans(plaintext, ciphertext)          #建立明文表与密文表的映射关系，存储在table里
    replace = text.translate(table)                      #使用table里的映射关系对text加密得到replace
    return replace


if __name__ == '__main__':
    plaintext = input("请输入明文：")
    #plaintext = 'Open Box PassWord:2021'
    print("得到密文为：", caesar_cipher(plaintext), sep='')
    