def affine_transform(input_str):
    affine_table = '1234567890_ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    transformed_str = ""
    signal = 0
    for char in input_str:
        if char in affine_table:
            index = affine_table.index(char)
            if signal % 2 == 0:
                transformed_index = (25 * (index - 18)) % 37
            else:
                transformed_index = (24 * (index - 3)) % 37
            transformed_char = affine_table[transformed_index]
            transformed_str += transformed_char
        else:
            transformed_str += char
        signal += 1
    return transformed_str

def main():
    input_str = '04FOOTFRACD9'
    transformed_str = affine_transform(input_str)
    print("变换后的字符串为：", transformed_str)

if __name__ == "__main__":
    main()
