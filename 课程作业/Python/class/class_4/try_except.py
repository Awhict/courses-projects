# 异常处理
try:
    num = eval(input("请输入一个整数:"))
    print(num**2)
except:
    print("输入错误，输入的不是数字！")
