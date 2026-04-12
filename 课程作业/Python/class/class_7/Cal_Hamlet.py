# 词频统计
# 英文——Hamlet
def getText():
    txt = open("pythonProject\\class_7\\hamlet.txt","r").read( )
    txt = txt.lower()
    for ch in '!"#$%&()*+,-./:;<=>?@[\\]^_“{|}~':
        txt = txt.replace(ch, " ") 
    return txt

hamletTxt = getText()
words = hamletTxt.split() 
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
excludes = {"the", "and", "to", "of", "you", "i", "a", "my", "in", "it", "that", "is", "not", "his", 
            "this", "but", "with", "for", "your", "me", "be", "as", "he", "what", "him"}
for word in excludes:
    del counts[word]
items = list(counts.items())
items.sort(key=lambda x:x[1], reverse=True) 
for i in range(10):
    word, count = items[i]
    print("{0:<10}{1:>5}".format(word, count) )
