import turtle
import math

# 最大圆半径240，最小圆的半径是60，由大到小依次减少60
# 由外向内填充颜色依次是红、白、红、蓝
turtle.speed(0) #设置turtle的速度为最快
color_list=['red','white','red','blue'] #填充颜色
xy_list=[(0,-240),(0,-180),(0,-120),(0,-60)] #从大到小四个圆的起始点坐标
#=======================================================
# 补充你的代码
for i in range(4):
    turtle.penup()
    turtle.goto(xy_list[i])
    turtle.pendown()
    turtle.pencolor(color_list[i])
    turtle.fillcolor(color_list[i])
    turtle.begin_fill()
    turtle.circle(240 - 60*i, 360)
    turtle.end_fill()
#=======================================================

# 内接五角星的边长，数学问题
width = (math.sin(math.radians(36)) * 60) / math.sin(math.radians(126))
# 绘制内接五角，填充白色
turtle.penup()
turtle.goto(0,60) #画笔移动到最小圆的最高点
turtle.pendown()
turtle.right(72) #设置画笔起始角度
turtle.pencolor('white') #设置画笔颜色为白色
turtle.fillcolor('white') #设置填充颜色为白色
turtle.begin_fill() #开始填充
for i in range(5):  #循环画五角星的外轮廓
    turtle.fd(width)
    turtle.left(72)
    turtle.fd(width)
    turtle.right(144)
turtle.end_fill() #结束填充
#=======================================================
# turtle.hideturtle()
turtle.done()