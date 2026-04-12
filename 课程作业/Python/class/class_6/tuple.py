# 元组:一旦创建不能修改
tuple1 = 0, 1, 2, 3
print(tuple1)
tuple2 = (0x001100, 'blue', tuple1)
print(tuple2)
print(tuple2[-1][2])
print(max(tuple1))
tuple3 = 'a', 'b', 'c'
print(max(tuple3))
