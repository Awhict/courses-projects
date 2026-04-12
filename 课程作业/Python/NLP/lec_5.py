# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 07:05:47 2024

@author: pathouli
"""

from utils import *

the_path = "C:/Users/pathouli/Box Sync/myStuff/academia/torhea/gen_lecture/data/data/"
out_path = "C:/Users/pathouli/Box Sync/myStuff/academia/torhea/gen_lecture/output/"

#the_data = file_crawler(the_path)

#pd_slice = the_data[the_data["label"] == "mathematics"]
#str_cat = pd_slice["body"].str.cat(sep=" ")

#we will build a function that outputs a dictionary where each key
#represents each unique topic and the value is a dictionary of the 
#word frequency for that respective topic

#word_f_fun = word_dict_fun(the_data, "body")

#print (rem_sw("the cable guy is almost here"))

#the_data["body_sw"] = the_data.body.apply(rem_sw)

#word_f_fun_sw = word_dict_fun(the_data, "body_sw")

#the_data["body_sw_stem"] = the_data.body_sw.apply(stem_fun)

#write_pickle(the_data, "the_data", out_path)

the_data = read_pickle(out_path, "the_data")

#   stem_fun("fishing is fun on the weekends")

#word_f_fun_stem = word_dict_fun(the_data, "body_sw_stem")

xform_data = t_form_fun(the_data, "body_sw_stem", 1, 1, "vec")

#all_cos, ind_cos = cos_fun(xform_data, the_data.label)

dim_data = pca_fun(xform_data, "0.95")



#chi-square, cosine_sim, embedding