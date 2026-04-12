height, weight = eval(input("请输入你的身高(m)和体重(kg):"))
bmi = weight / pow(height, 2)
print("BMI数值为:{:.2f}".format(bmi))

if bmi < 18.5:
    print("偏瘦")
elif bmi < 23.9:
    print("正常")
elif bmi < 28:
    print("偏胖")
else:
    print("肥胖")
