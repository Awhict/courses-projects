# 计算一天内的时间差
a, b, c, d = map(int, input().split(" "))

start = a * 60 + b
finish = c * 60 + d
spend = finish - start

e = spend // 60
f = spend % 60

print(e, f)
