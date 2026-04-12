# 存款买房——无涨薪
total_cost = float(input())           # total_cost为当前房价
annual_salary = float(input())        # 年薪
portion_saved = float(input()) / 100  # 月存款比例，输入30转为0.30（即30%）

# 根据首付款比例计算首付款down_payment，根据月存款比例计算月存款额monthly_deposit
#=======================================================
portion_down_payment = 0.30
down_payment = total_cost * portion_down_payment
monthly_deposit = annual_salary / 12 * portion_saved
#=======================================================
print('首付 {:.2f} 元'.format(down_payment))
print('月存款 {:.2f} 元'.format(monthly_deposit))

# 计算多少个月才能存够首付款，结果为整数，不足1月按1个月计算，即向上取整
#=======================================================
if down_payment // monthly_deposit == 0:
    number_of_months = down_payment // monthly_deposit
else:
    number_of_months = down_payment // monthly_deposit + 1
#=======================================================
print(f'需要{int(number_of_months)}个月可以存够首付')
