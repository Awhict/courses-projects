import math

def distance(x, y, z):
    a = x*x + y*y + z*z
    b = pow(a, 0.5)
    return b

x,y,z=input().split(",")
d=distance(float(x),float(y),float(z)) #调用distance函数
print("{:.2f}".format(d))              #输出距离值，保留两位小数

#代码区结束