# 集合的创建
a = {'python', 123, ('python', 123)}
b = set('pypy123')
c = {'python', 123, 123, 456}
d = set()  # 空集只能用set创建，不能用{}创建
print(a)
print(b)
print(c)
print(d)
print('-'*30)

# 集合的运算:并|、交&、差-、补^
print(a | c)
print(a & c)
print(a - c)
print(a ^ c)
print('-'*30)

# 集合处理函数
d.add(1)
d.add(2)
d.discard(0) # 不会报错
d.remove(1)  # 会报错
d.pop()  # 集合为空时报错
d.clear()
d.copy() # 返回一个副本
len(d)
1 in d  # True
1 not in d  # False

# 数据去重
ls = [1,1,2,3,4,5,4,3]
print(ls)
s = set(ls)
lt = list(s)
print(lt)
