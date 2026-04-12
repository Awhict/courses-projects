# 列表:可变组合数据类型
ls = [1,2,3,4]
lt = ls   # 传递索引而非复制
ls[-1] = 10
print(ls)
print(lt)
print('-'*20)

# 列表操作
ls = [i for i in range(20)]
print(ls)
ls[2:9] = [0,0,0,0,0,0,0]
print(ls)
del ls[::2]
print(ls)
ls.append('a')
print(ls)
lt = ls.copy()
lt.insert(3, 'hihihi')
print(lt)
ls.reverse()
print(ls)
print(ls.index(1))
