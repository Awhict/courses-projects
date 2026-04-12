# 沉默的羔羊之最多单词
import jieba
from collections import Counter
 
# 读取文件内容
file_path = "沉默的羔羊.txt"
with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()
 
# 分词
words = list(jieba.cut(content))
 
# 过滤长度大于2的单词
filtered_words = [word for word in words if len(word) > 2]
 
# 计算词频
word_frequency = Counter(filtered_words)
 
# 找到最多的单词
most_common_words = word_frequency.most_common()
 
# 如果存在多个单词出现频率一致，请按照Unicode排序
most_common_words.sort(key=lambda x: (x[1], x[0]), reverse=True)
 
# 输出结果
if most_common_words:
    max_word, max_count = most_common_words[0]
    print(f"{max_word}")
