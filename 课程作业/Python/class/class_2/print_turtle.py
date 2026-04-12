import turtle
# 对象.方法()  or  库.函数()
turtle.setup(650, 350, 200, 200)  # 画框/画布(长, 宽, x起始, y起始)
turtle.penup()                    # 提笔
turtle.fd(-250)                   # 移动（移动距离）
turtle.pendown()                  # 落笔
turtle.pensize(25)                # 笔迹大小
turtle.pencolor("green")          # 笔迹颜色
turtle.seth(-40)                  # 转动（转动角度）
for i in range(4):
    turtle.circle(50, 80)         # 画圆（半径，角度）
    turtle.circle(-40, 80) 
turtle.circle(40, 80/2) 
turtle.fd(40)
turtle.circle(16, 180) 
turtle.fd(40 * 2/3)
turtle.done()                     # 停止