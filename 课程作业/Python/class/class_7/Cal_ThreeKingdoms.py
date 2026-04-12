# 词频统计
# 中文——三国演义
import jieba
txt = open("PythonProject/class/class_7/threekingdoms.txt","r", encoding="utf-8").read() 
words = jieba.lcut(txt) 
counts = {}
for word in words:
    if len(word) == 1: #把单字去掉，古文中2字及以上的大概率是人名
        continue
    elif word == '玄德曰' or word == '玄德':
        rword = '刘备'
    elif word == '孔明曰' or word == '诸葛亮':
        rword = '孔明'
    elif word == '云长' or word == '关公':
        rword = '关羽'   
    else:
        rword = word 
    counts[rword] = counts.get(word,0) + 1
excludes = {"将军", "却说", "丞相", "二人", "不可", "荆州", "不能", "如此", "商议", "如何", "主公", "军士", "军马", "一人", 
            "不知", "汉中", "只见", "众将", "后主", "左右", "次日", "引兵", "大喜", "天下", "东吴", "于是", "今日", "不敢", 
            "魏兵", "陛下", "都督", "人马", "蜀兵", "上马", "大叫", "太守", "此人", "夫人", "先主", "后人", "背后", "天子"}
for word in excludes:
    del counts[word]
items = list(counts.items())
items.sort(key=lambda x:x[1], reverse=True) 
for i in range(15):
    word, count = items[i]
    print("{0:<10}{1:>5}".format(word, count))
