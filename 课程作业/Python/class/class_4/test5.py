#字符串头尾拼接
str = input()
head = str.split('-')[0]
tail = str.split('-')[-1]
print(head + '+' + tail)
