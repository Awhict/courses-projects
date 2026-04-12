import turtle
turtle.setup(650, 450, 200, 200) # 设置窗口大小和位置
turtle.penup()                   # 抬起画笔
turtle.fd(-180)
turtle.pendown()
turtle.pensize(3)
turtle.pencolor("#FF0000")       # 设置画笔颜色
for i in range(5):
    turtle.fd(300)
    turtle.right(144)
turtle.done()