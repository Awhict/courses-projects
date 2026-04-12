import wordcloud
import jieba


# 英文词云
w = wordcloud.WordCloud()
# 可配置参数：width  height  min_font_size  max_font_size  font_step  stopword  mask  colormap ...
txt1 = "wordcloud by python"
w.generate(txt1)
w.to_file("word_cloud_en.png")


# 中文词云
c = wordcloud.WordCloud(font_path="msyh.ttc", width=1000, height=700)
txt2 = "北京邮电大学计算机学科计算机指令编程语言"
c.generate(" ".join(jieba.lcut(txt2)))
c.to_file("word_cloud_cn.png")
