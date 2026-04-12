# 计算圆周率——割圆法
import math


def cutting_circle(times):   # times为分割次数
    """接收表示分割次数的整数n为参数, 计算分割n次时正多边形的边数和圆周率值, 返回边数和圆周率值"""
    side_length = 1          # 初始边长
    edges = 6                # 初始边数
    while times:
        point_to_pedal = (1 - (0.5 * side_length) ** 2) ** 0.5
        edge_to_pedal = 1 - point_to_pedal
        side_length = ((0.5 * side_length) ** 2 + edge_to_pedal ** 2) ** 0.5
        edges *= 2
        times -= 1
    pi = side_length * edges / 2
    return edges, pi


if __name__ == '__main__':
    times = int(input())          # 割圆次数
    print('分割{}次，边数为{}，圆周率为{:.6f}'.format(times, *cutting_circle(times)))          # 圆周率
    print('math库中的圆周率常量值为{:.6f}'.format(math.pi))
