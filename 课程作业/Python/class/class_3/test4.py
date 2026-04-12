# lucky word

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


str = input()
char_count = [0] * 26

for i in range(len(str)):
    char_count[ord(str[i]) - 97] += 1

char_count = [i for i in char_count if i]

maxn = max(char_count)
minn = min(char_count)
sub = maxn - minn

if isPrime(sub):
    print("Lucky Word")
    print(sub)
else:
    print("No Answer")
    print(0)
