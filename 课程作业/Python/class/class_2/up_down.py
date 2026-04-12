import math

up = pow(1.001, 365)
down = pow(0.999, 365)
print(up)
print(down)

x = 1
for i in range(365):
    if 365%7 in [1, 2, 3, 4, 5]:
        x *= 1.001
    elif 365%7 in [0, 6]:
        x *= 0.999
print(x)