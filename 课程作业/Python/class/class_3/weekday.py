weekstring = '星期一星期二星期三星期四星期五星期六星期天'
weekid = eval(input('请输入星期数(1-7):'))
pos = (weekid - 1) * 3
print(weekstring[pos : pos+3])