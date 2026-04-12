'''
时间获取:
time() ctime() gmtime()
时间格式化:
strftime() strptime()
程序计时:
sleep() perf_counter()
'''
import time
# 从1970-1-1 0:00:00开始到目前的时间
time.time()

# 以字符串形式返回时间
time.ctime()

# 返回一个CPU级别的精确时间，需要连续调用才有意义
start = time.perf_counter()
during = time.perf_counter() - start

# 程序休眠
time.sleep(10)
