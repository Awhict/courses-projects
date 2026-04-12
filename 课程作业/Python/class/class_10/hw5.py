# 文件关键行数
with open('latex.log','r',encoding='utf-8') as f: 
    rows_set = set(f.readlines()) # 去除重复行用set去重
print('共{}关键行'.format(len(rows_set))) # format标准化输出 len直接取set的长度
