# 匿名函数
f1 = lambda x, y : x + y
print(f1(10, 15))

f2 = lambda : 'lambda function'
print(f2())


# 使用普通函数
def sq(x):
    return x*x
aa = map(sq, [y for y in range(10)])
print(list(aa))
# 使用匿名函数
bb = map(lambda x : x*x, [y for y in range(10)])
print(list(bb))
