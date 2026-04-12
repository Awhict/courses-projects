# 哪一天不开心
now = result = 0

for i in range(1,8):
    a, b = map(int, input().split(' '))
    sum = a + b
    if sum > 8:
        if sum > now:
            result = i
            now = sum
    # print(result)

print(result)
