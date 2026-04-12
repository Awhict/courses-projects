# 鸡兔同笼
a, b = map(int,input().split(' '))
if a > 0 and b > 0 and b % 2 == 0:
    chick = 2 * a - b // 2
    rabbit = b // 2 - a
    if chick >= 0 and rabbit >= 0:
        print(f'有{chick}只鸡，{rabbit}只兔')
    else:
        print('Data Error!')
else:
    print('Data Error!')
