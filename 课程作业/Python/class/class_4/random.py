import random
# 0-1的随机数
random.random()

# 选择范围内的随机数
random.uniform(0,9)

a = [1,2,3,4,5,6,7,8,9]
# 从对象中选择一个
random.choice(a)
# 从对象中选择多个
random.choices(a, k=2)
# 洗牌
random.shuffle(a)

# 随机数种子：种子相同，生成的随机数序列也相同，便于测试与复现
random.seed(10)
