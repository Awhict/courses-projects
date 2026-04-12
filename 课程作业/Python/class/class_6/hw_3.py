# 二鼠打洞
wall = int(input()) #墙壁的厚度
rat, mouse, day, time = 1, 1, 0, 1 #大鼠速度、小鼠速度、天数、当天工作时长（1表示工作一整天）
distance_of_rat, distance_of_mouse = 0, 0 #大鼠路程、小鼠的路程
while wall > 0:
    if wall-rat-mouse < 0:
        time = wall / (rat+mouse)
        break
    wall -= (rat+mouse) #剩余墙厚
    day += 1
    distance_of_rat += rat
    distance_of_mouse += mouse
    rat *= 2
    mouse /= 2
if time < 1:
    day += 1
distance_of_rat += rat*time
distance_of_mouse += mouse*time

print(day)
print(round(distance_of_mouse, 1), round(distance_of_rat, 1)) 
