def find_inverse_element(a, n):
    t, new_t = 0, 1
    r, new_r = n, a

    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r

    if r > 1:
        raise ValueError("a在模n下没有逆元")
    if t < 0:
        t = t + n
    
    return t


def main():
    print("该程序用于计算a模n的逆元")
    a = int(input("请输入a的值: "))
    n = int(input("请输入n的值: "))
    print(f"{a}模{n}的逆元为：{find_inverse_element(a, n)}")

if __name__ == "__main__":
    main()
