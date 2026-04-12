# 个人所得税计算器
salary = float(input())                   # salary 应发工资薪金所得
five_one_insurance_fund = float(input())  # five_one_insurance_fund  五险一金
exemption = float(input())                # exemption 个税免征额
if salary <= 0:
    print('error')
else:
    salary_for_tax = salary - five_one_insurance_fund - exemption
    if salary_for_tax < 0:
        tax = 0
    elif salary_for_tax < 3000:
        tax = salary_for_tax * 0.03
    elif salary_for_tax < 12000:
        tax = salary_for_tax * 0.10 - 210
    elif salary_for_tax < 25000:
        tax = salary_for_tax * 0.20 - 1410
    elif salary_for_tax < 35000:
        tax = salary_for_tax * 0.25 - 2660
    elif salary_for_tax < 55000:
        tax = salary_for_tax * 0.30 - 4410
    elif salary_for_tax < 80000:
        tax = salary_for_tax * 0.35 - 7160
    else:
        tax = salary_for_tax * 0.45 - 15160
    final_salary = salary - five_one_insurance_fund - tax
    print('应缴税款{:.2f}元，实发工资{:.2f}元。'.format(tax,final_salary))

