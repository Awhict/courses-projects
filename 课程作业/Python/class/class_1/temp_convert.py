#TempConvert.py

temp_str = input('请输入带有符号的温度值:')
if temp_str[-1] in ['F','f']:
    C = (eval(temp_str[0:-1]) - 32) / 1.8 
    print('转换后的温度是{:.2f}C'.format(C)) 
elif temp_str[-1] in ['C','c']:
    F=1.8 * eval(temp_str[0:-1]) + 32
    print('转换后的温度是{:.2f}F'.format(F)) 
else:
    print('输入格式错误')