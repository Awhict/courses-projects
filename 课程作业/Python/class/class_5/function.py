# 函数
def fac1(n):
    s = 1
    for i in range(1, n+1):
        s *= i
    return s


# 函数参数缺省：给出默认值
def fac2(n, m=1):
    s = 1
    for i in range(1, n+1):
        s *= i
    return s//m


# 未知数量的参数：用*指定
def fac3(n, *m):
    s = 1
    for i in range(1, n+1):
        s *= i
    for item in m:
        s *= item
    return s


# 传参方式
a = fac2(10, 2)          # 位置传参
b = fac3(m = 2, n = 10)  # 名称传参


# 多个返回值：返回值类型为元组
def fac4(n, m=1):
    s = 1
    for i in range(1, n+1):
        s *= i
    return s//m, n, m
# 多个返回值时的返回值接收
a, b, c = fac4(10, 2)


# 函数递归
def fac5(n):
    if n == 0:
        return 1
    else:
        return n*fac5(n-1)
# 调用递归函数
a = fac5(10)


# 斐波那契数列
def Fibonacci(n):
    if n == 1 or n == 2:
        return 1
    else:
        return Fibonacci(n-1) + Fibonacci(n-2)
a = Fibonacci(10)
