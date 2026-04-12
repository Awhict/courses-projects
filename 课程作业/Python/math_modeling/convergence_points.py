# 求解差分方程的收敛点
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def logistic_map(x, b):
    return b * x * (1 - x)

def find_convergence(x0, b, tol=1e-8, max_iter=1000):
    x = x0
    for _ in range(max_iter):
        x_next = logistic_map(x, b)
        if abs(x_next - x) < tol:
            return x_next
        x = x_next
    return None

# 1. 计算差分方程的收敛点
convergence_points = []
b_values = np.arange(2.5, 3.51, 0.01)
for b in b_values:
    x0 = 0.5  # 初始值
    convergence_point = find_convergence(x0, b)
    if convergence_point is not None:
        convergence_points.append(convergence_point)

# 2. 记录不同b值的收敛点并导出为CSV表格
data = pd.DataFrame({'b_values': b_values[:len(convergence_points)], 'convergence_points': convergence_points})
data.to_csv('convergence_points.csv', index=False)

# 3. 读取CSV表格，绘制散点图
data = pd.read_csv('convergence_points.csv')
plt.scatter(data['b_values'], data['convergence_points'], s=5)
plt.xlabel('b')
plt.ylabel('Convergence Point')
plt.title('Convergence Points vs. b')
plt.show()
