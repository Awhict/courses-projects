# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 07:05:47 2024

@author: pathouli
"""

from utils import *

the_path = "E:\Project\Python\pythonProject\NLP\data"

the_data = file_crawler(the_path)

pd_slice = the_data[the_data["label"] == "mathematics"]
str_cat = pd_slice["body"].str.cat(sep=" ")

#we will build a function that outputs a dictionary where each key
#represents each unique topic and the value is a dictionary of the 
#word frequency for that respective topic

word_f_fun = word_dict_fun(the_data, "body")

print (rem_sw("the cable guy is almost here"))

the_data["body_sw"] = the_data.body.apply(rem_sw)

word_f_fun_sw = word_dict_fun(the_data, "body_sw")

#fish fishes fished fishing
#stemming removes affixes and resultant is the ROOT word
#lemmatization removes affixes and resultant is the ROOT word
#lemmatization guaranteed a word in dictionary
#print (stem_fun(test_corpus))

the_data["body_sw_stem"] = the_data.body_sw.apply(stem_fun)

stem_fun("fishing is fun on the weekends")

word_f_fun_stem = word_dict_fun(the_data, "body_sw_stem")

test = t_form_fun(the_data, "body", 1, 3)

#test = word_freq_fun(str_cat)
#next week pick up here with word freq by topics