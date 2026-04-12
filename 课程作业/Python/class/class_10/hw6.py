# 中文词语逆序
import jieba
s = input()
s1 = list(jieba.lcut(s))
s2 = "".join(s1[::-1])
print(s2)
