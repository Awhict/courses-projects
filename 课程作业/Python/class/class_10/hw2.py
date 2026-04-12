input_str = input()
dic = eval(input_str)
# dic = {"a":1,"b":2,"c":3}
try:
    inverse_dic = {}
    for key,val in dic.items():
        inverse_dic[val] = key
    print(inverse_dic)
except:
    print("输入错误")
    