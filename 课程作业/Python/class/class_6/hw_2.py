# 物不知数
n = eval(input())
flag = 0
for i in range(n+1):
    if i%3==2 and i%5==3 and i%7==2:
        flag += 1
        print(i)
if flag == 0:
    print('No solution!')
