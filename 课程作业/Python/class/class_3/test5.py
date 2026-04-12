# 哥德巴赫猜想
import ast
n = ast.literal_eval(input())

def isPrime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    maxFactor = round(n**0.5)
    for factor in range(3, maxFactor+1, 2):
        if n % factor == 0:
            return False
    return True

for i in range(4, n+1, 2):
    for j in range(2, n//2):
        if isPrime(j) and isPrime(i-j):
            print("{}={}+{}".format(i, j, i-j))
            break
