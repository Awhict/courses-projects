# 字典:键值对的集合 {<键>:<值>}
# 键唯一，值可以不唯一
d = {'中国':'北京', '法国':'巴黎', '英国':'伦敦'}
print(d['中国'])
print(d.keys())
print(d.values())
print(d.items())
print(len(d))
print(d.pop('中国', 'NULL'))
print(d.get('中国', 'NULL'))
print(d.popitem())
