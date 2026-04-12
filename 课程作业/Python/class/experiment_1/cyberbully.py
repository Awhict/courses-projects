import random


def ReadFile(filepath):
    '''此函式接收一个文件路径并读取该文件，将文件内容作为字符串返回'''
    with open(filepath, "r", encoding="utf-8") as file:
        rawdata = file.read().replace('\n', '')
    return rawdata


def CleanData(text):
    '''此函数利用正则表达式对数据进行清理，函数输入为待处理文本，返回值为清理后的文本'''
    import re
    text = re.sub('[、#：:【】\[\]！，。@/？]+', '', text)
    return text


def RemoveStopwords(text):
    """此函数用于去除文本中的停用词，函数输入为待处理文本，返回值为去除停用词后的文本"""
    import jieba
    import jieba.analyse
    seg_list = jieba.cut(text)
    cleaned_text = ''
    # 停用词列表如下：
    stopwords = ['我', '你', '他', '她', '它', '的', '地', '得', '或', '与', '等', '是', '有', '和', '被', '把', '之', '也', '吗', '于', '中','四川', '大学', '回应', '网传', '视频', '回复', '转发', '允悲', '战于野', '张忆安', '平移']
    for word in seg_list:
        if word not in stopwords:
            cleaned_text += word
    return cleaned_text


def ExtractKeyTFIDF(text, k):
    '''此函数利用TF-IDF算法提取文本关键词, 函数输入为待处理文本与关键词数量, 返回值为关键词列表'''
    import jieba.analyse
    keywords = jieba.analyse.extract_tags(sentence = text, # 文本内容
                                          topK = k, # 提取的关键词数量
                                          allowPOS = ['n','nz','v', 'vd', 'vn', 'ns', 'nr'], # 允许的关键词的词性
                                          withWeight = False, # 是否附带词语权重
                                          withFlag = False # 是否附带词语词性
                                          )
    return keywords


def ExtractKeyTextRank(text, k):
    '''此函数利用TextRank算法提取文本关键词, 函数输入为待处理文本与关键词数量, 返回值为关键词列表'''
    import jieba.analyse
    keywords = jieba.analyse.textrank(sentence = text,    # 文本内容
                                      topK = k,   # 提取的关键词数量
                                      allowPOS = ['n','nz','v', 'vd', 'vn', 'ns', 'nr'],  # 允许的关键词的词性
                                      withWeight = False,  # 是否附带词语权重
                                      withFlag = False   # 是否附带词语词性
                                     )
    return keywords


def DetectSensitiveWords(text_list, sensitive_words):
    """此函数用于检测文本列表中是否包含敏感词汇，输入为待检测文本列表和敏感词汇列表，输出为含有敏感词汇的文本列表"""
    sensitive_texts = []
    for text in text_list:
        for word in sensitive_words:
            if word in text:
                sensitive_texts.append(text)
                break  # 一旦发现敏感词，就跳出内层循环，检测下一个文本
    return sensitive_texts


def CyberStatistic(processed_texts, original_texts):
    """此函数用于网暴数据result进行统计"""
    # 计算处理后的文本条数占处理前的文本条数的百分比
    percentage = (len(processed_texts) / len(original_texts)) * 100
    # 绘制饼状图
    import matplotlib.pyplot as plt
    labels = ['Processed Texts', 'Original Texts']
    sizes = [len(processed_texts), len(original_texts) - len(processed_texts)]
    explode = (0.1, 0)  # 突出显示处理后的文本部分
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Text Processing Percentage: {:.2f}%'.format(percentage))
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()



if __name__ == "__main__":
    # 仅提供一种常用思路————采用二维列表的方式存储对应的网暴言论
    CyberList = []
    # 读文件操作
    with open("pythonProject\\experiment_1\\review.txt", "r", encoding="utf-8") as file:
        data = file.readlines()
    # 打印网暴数据数量
    print(len(data))
    # 打印前5条数据
    print(data[:5])
    # 随机打印2条数据
    print(random.choices(data, k = 2))

    # 读文件，返回一个字符串
    raw_data = ReadFile("pythonProject\\experiment_1\\review.txt")

    # 对读入的数据进行清理
    cleaned_data = CleanData(raw_data)

    # 去除文本中的停用词
    new_data = RemoveStopwords(cleaned_data)
    
    # 使用 jieba 进行 TF-IDF 算法提取文本关键词
    keywords = ExtractKeyTFIDF(new_data, 10)
    #print(keywords)

    # 使用 jieba 进行 textrank 算法提取文本关键词
    #keywords = ExtractKeyTextRank(new_data, 10)
    #print(keywords)

    '''
    # 示例待检测文本列表
    text_list = ["这是一段正常文本。", "这里可能含有敏感词汇如赌博。", "请勿发送不当言论。"]
    # 示例敏感词汇列表
    sensitive_words = ["赌博", "不当言论"]
    # 检测含有敏感词汇的文本列表
    result = detect_sensitive_words(text_list, sensitive_words)
    print("含有敏感词汇的文本列表：", result)
    '''
    # 检测含有敏感词汇的文本列表，得到对应的网暴言论
    sens_words = ['网暴', '血口喷人', '装什么', '恶心', '该死', '祖宗', '装逼', '草泥马', '特么的', '撕逼']
    #print(sens_words)
    sens_words.extend(keywords)
    print(sens_words)
    result = DetectSensitiveWords(data, sens_words)
    print("含有敏感词汇的文本列表(随机十条):", random.choices(result, k = 10), sep='\n')
    
    # 进行数据统计
    CyberStatistic(result, data)
