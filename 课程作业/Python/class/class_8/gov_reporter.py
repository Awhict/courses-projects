import wordcloud
import jieba
import numpy as np

with open("pythonProject\class_8\gov_reporter.txt", "r", encoding="utf-8") as file:
    txt = file.read()

x, y = np.ogrid[:300, :300]
mk = (x - 150)**2 + (y - 150)**2 > 150**2
mk = 255 * mk.astype(int)

excludes = ['的', '和', '等', '大', '对', '要', '了', '在', '以上']

c = wordcloud.WordCloud(
    font_path="msyh.ttc", 
    mask=mk, 
    stopwords=excludes, 
    min_font_size=12, 
    background_color='white'
    )

c.generate(" ".join(jieba.lcut(txt)))
c.to_file("gov_reporter.png")
