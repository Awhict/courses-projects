PM = eval(input("请输入一个数字(0-100):"))
if PM > 75:
    print("Bad")
elif PM >35:
    print("Normal")
else:
    print("Good")

print("-"*30)
print("空气{}污染".format("严重" if PM>=75 else "没有"))
