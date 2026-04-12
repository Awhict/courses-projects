# 数据的组织：一维、二维、n维
# 一维数据：列表、集合；
# 二维数据：多个一维数据组成；
# 高维数据：json、键值对。

# 数据的操作周期：
#   存储  <->  表示  <->  操作
# 存储格式<->数据类型<->操作方式

# 数据的表示与存储：
# 一维数据
# 表示：
ls1 = [1.23, 2.34, 3.45] # <- 一层for循环遍历
# 存储：空格分隔、符号分隔、标签分隔
# 处理：读入、处理、写入、保存
# f = open(fname, w)
# f.write(" ".join(ls))
# f.close()
# 二维数据
# 表示：
# ls2 = [[1,2,3], [4,5,6], [7,8,9]] # <- 两层for循环遍历
ls2 = [0, 1, 2]
ls2[0] = [1, 2, 3]
ls2[1] = [4, 5, 6]
ls2[2] = [7, 8, 9]
for line in ls2:
    for row in line:
        print(line, row)
print(f'在索引为(1,1)处的值为{ls2[1][1]}')

# csv格式(comma seperate value, 逗号分隔数据) -> 常用于保存二维数据

# 高维数据
# 键值对形式->"key":"value"->json格式
import json  # json库
json.dumps() # python数据结构->json格式
json.loads() # json格式->python数据格式(字典、列表)
