# 求解线性规划
import numpy as np
import matplotlib.pyplot as plt
from pulp import *

# 创建线性规划问题
def create_lp_problem(k_value):
    prob = LpProblem("Minimize_R", LpMinimize)

    # 定义变量
    x0 = LpVariable("x0", lowBound=0)
    x1 = LpVariable("x1", lowBound=0)
    x2 = LpVariable("x2", lowBound=0)
    x3 = LpVariable("x3", lowBound=0)
    x4 = LpVariable("x4", lowBound=0)
    k = LpVariable("k", lowBound=0)  # 额外定义k

    # 定义目标函数
    prob += 0.025*x1 + 0.015*x2 + 0.055*x3 + 0.026*x4, "Objective Function"

    # 定义约束条件
    prob += x0 + 1.01*x1 + 1.02*x2 + 1.045*x3 + 1.065*x4 == 1, "Constraint1"
    prob += 0.05*x0 >= k, "Constraint2"
    prob += 0.27*x1 >= k, "Constraint3"
    prob += 0.19*x2 >= k, "Constraint4"
    prob += 0.185*x3 >= k, "Constraint5"
    prob += 0.185*x4 >= k, "Constraint6"
    
    # 设置k值
    prob.constraints["Constraint2"] = k_value
    prob.constraints["Constraint3"] = k_value
    prob.constraints["Constraint4"] = k_value
    prob.constraints["Constraint5"] = k_value
    prob.constraints["Constraint6"] = k_value

    # 求解问题
    prob.solve()

    return value(prob.objective)

# 求解多个k值对应的线性规划问题并保存结果
k_values = np.arange(0, 0.271, 0.001)
R_values = []
for k_value in k_values:
    R_values.append(create_lp_problem(k_value))

# 绘制散点图
plt.scatter(k_values, R_values, s=5)
plt.xlabel('k')
plt.ylabel('R')
plt.title('k vs. R')
plt.grid(True)
plt.show()
