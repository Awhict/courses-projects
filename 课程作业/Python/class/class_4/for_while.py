for i in range(1,20,3):   # 取不到末尾值(左闭右开)——range
    print(i, end=' ')
print()

for i in "python":        # 能取到末尾值(闭区间)——字符串、列表、文件
    print(i, end=' ')
else:
    print("循环正常结束")
print()

for i in range(10):
    if i == 4:
        continue
    if i == 7:
        break
    print(i)
print()

for s in "BIT":
    for i in range(10):
        print(s, end='')
        if s == "I":
            break
print()

for s in "python":
    print(s, end=' ')
    if s == "t":
        continue
else:
    print("循环正常结束")
print()
for s in "python":
    print(s, end=' ')
    if s == "t":
        break
else:
    print("循环正常结束")
print()