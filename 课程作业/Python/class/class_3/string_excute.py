# 大小写转化
print(str.upper('abcdefg'))
print(str.lower('UVWXYZ'))
print('-'*50)

# 字符串分割
astr = '一,二,三,四,五'
print(astr.split(','))
print(astr.split(',')[2])
astr = astr.split(',')
print('-'*50)

# 查询子串数目
bstr = 'an apple a day'
print(bstr.count('a'))
print('-'*50)

# 字符串替换(所有字符)
print(bstr.replace('a', '2'))
print('-'*50)

# 字符串居中(返回值为字符串)
cstr = 'python'
cstr = cstr.center(20, '=')
print(cstr)
print('-'*50)

# 字符串去除(两边都去除)
cstr = cstr.strip('=')
print(cstr)
print('-'*50)

# 字符串添加
print('-'.join(astr))
print('-'*50)

# 字符串的格式化输出
# format()方式:{<参数序号>:<格式控制标记>}
#                          格式控制标记————填充，对齐，宽度，千分位分隔符，精度，类型
print("{}: 计算机{}的CPU占用率为{}%".format("xx", "yy", "zz"))
print("{1}: 计算机{2}的CPU占用率为{0}%".format("xx", "yy", "zz"))
print('{:*>20}'.format('bbs'))
print('{:.2f}'.format(1234.5678))
print('-'*50)

# 字符串与列表相互转化
str1 = 'This works but is confusing'
str2 = list(str1.split(' '))
str2 = str2[::-1]
print(str2)
str3 = ' '.join(str2)
print(str3)