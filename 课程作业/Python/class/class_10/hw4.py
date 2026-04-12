# 数字不同数之和
num = input()
s = set(num)
sum = 0
for i in s:
    sum += eval(i)
print(sum)
