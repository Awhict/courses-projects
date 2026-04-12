n, s = 10, 100  # 这是全局变量:global varible

def fac(n):
    s = 1  # 这是局部变量:local varible
    for i in range(1, n+1):
        s *= i
    return s

print(fac(n), s)

def fac1(n):
    global s # 在函数内使用全局变量
    for i in range(1, n+1):
        s *= i
    return s

ls = ['a','b']
def func(a):
    # ls = []
    ls.append(a) # 组合数据类型若未创建新值则默认为全局变量
    return ls
ls = func('c')
print(ls)
