import jieba
s = "南京市长江大桥"
news = "江大桥"
jieba.lcut(s, cut_all=True) # 全模式
jieba.lcut_for_search(s)    # 搜索引擎模式
jieba.lcut(s)               # 精确模式
jieba.add_word(news)
