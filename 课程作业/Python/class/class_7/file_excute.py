# 文件操作

# 打开文件
tf = open("file.txt", "at", encoding="utf-8")

# 文件读取
tf.read()  # 读全部->返回字符串
tf.readline()  # 读一行->返回列表, 配合while使用
tf.readlines()  # 读多行->返回列表

# 关闭文件
tf.close()

# 快捷读文件操作（省略close操作）
with open("file.txt", "r", encoding="utf-8") as file:
    data = file.readlines()

# 绝对路径与相对路径
# 绝对路径——从根目录寻找文件
# 相对路径——从终端当前位置开始寻找文件

# 打开模式：
# r(只读)  w(覆盖写)  x(创建写)  a(追加写)
# b(二进制形式)  t(文本形式)  +(同时读写)

# 文件写入
tf.write("blahblah")
ls = ['123','456','789']
tf.writelines(ls) # 将列表内容写入，不加空格和换行
tf.seek() # offset: 0-文件开头 1-当前位置 2-文件末尾
