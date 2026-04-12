#凯撒密码————解密
import string


def caesar_decrypt(text, offset):
    """
    接收一个加密的字符串text和一个整数offset为参数并采用字母表和数字中前面第offset个字符
    代替当前字符的方法对字符串中的字母和数字进行替换，实现解密效果，返回值为解密的字符串。
    """
    plaintext = ''
    for i in range(len(text)):
        if text[i].islower():
            plaintext += chr((ord(text[i]) - 97 - offset)%26 + 97)
        elif text[i].isupper():
            plaintext += chr((ord(text[i]) - 65 - offset)%26 + 65)
        elif text[i].isdigit():
            plaintext += chr((ord(text[i]) - 48 - offset)%10 + 48)
        elif not text[i].isalpha():
            plaintext += text[i]
    return plaintext


def find_offset(key_text, ciphertext):
    """
    接收一个单词和一个加密字符串为参数，尝试用[0,25]之间的数为偏移量进行解密。
    如果key_text在解密后的明文里则说明解密成功。
    找出偏移量数值并返回这个整数偏移量。
    """
    for i in range(26):
        plaintext = ''
        for j in range(len(ciphertext)):
            if ciphertext[j].islower():
                plaintext += chr((ord(ciphertext[j]) - 97 - i)%26 + 97)
            elif ciphertext[j].isupper():
                plaintext += chr((ord(ciphertext[j]) - 65 - i)%26 + 65)
            elif not ciphertext[j].isalpha():
                plaintext += ciphertext[j]
        #print(plaintext)
        if key_text in plaintext:
            return i


if __name__ == '__main__':
    key_message = 'question'                                     #密文中的已知单词
    #cipher_text = 'vzjxynts'
    cipher_text = 'Yt gj,tw sty yt gj,ymfy nx f vzjxynts.'       #截获的密文
    secret_key = find_offset(key_message, cipher_text)           #破解密码，得到密匙
    print(f'密钥是{secret_key}')
    
    target_text = input()                                        #读入新密文，进行解密
    #target_text = 'Fyyfhp ts Ujfwq Mfwgtw ts Ijhjrgjw 2, 6496'  #新密文，需要解密
    print(caesar_decrypt(target_text, secret_key))               #解密，打印明文
    