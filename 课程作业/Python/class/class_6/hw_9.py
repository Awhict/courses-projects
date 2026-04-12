# 计算圆周率——无穷级数法
def leibniz_of_pi(threshold):
    """接收用户输入的浮点数阈值为参数，返回圆周率值"""
    #=======================================================
    item = result = n = 0
    while True:
        last = (-1)**n / (2*n+1)
        if abs(last) < threshold:
            break
        item += last
        n += 1
        result = item * 4
    return result
    #=======================================================


if __name__ == '__main__':
    threshold = float(input())
    print("{:.8f}".format(leibniz_of_pi(threshold))) #保留小数点后八位
