def hex_to_ascii_inverse(hex_string):
    # 将十六进制字符串转换为整数
    num = int(hex_string, 16)
    
    # 将整数转换为二进制字符串（去掉前缀 '0b'）
    bin_string = bin(num)[2:]
    
    # 补齐二进制字符串为8的倍数（每个ASCII字符是8位）
    bin_string = bin_string.zfill((len(bin_string) + 7) // 8 * 8)
    
    # 按位取反
    inverted_bin_string = ''.join('1' if bit == '0' else '0' for bit in bin_string)
    
    # 将按位取反后的二进制字符串转换为整数
    inverted_num = int(inverted_bin_string, 2)
    
    # 将整数转换为ASCII字符
    ascii_char = chr(inverted_num)
    
    return ascii_char

# 输入一个十六进制字符串
# hex_string = "0xd5" 
# result = hex_to_ascii_inverse(hex_string)
 
hex_string = "0xBD,0x9A,0x9E,0x8B,0xD5,0xCF,0x92,0x96,0x9C,0x8D,0x90,0x91,0xD5,0xDE"
hex_string_list = hex_string.split(",")
result = ""
for hex_string in hex_string_list:
    ascii_result = hex_to_ascii_inverse(hex_string)
    result += ascii_result

# print(f"输入的十六进制数: {hex_string}")
print(f"解出的flag为: {result}")
