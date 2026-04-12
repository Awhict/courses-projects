# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 07:12:13 2024

@author: pathouli
"""

from utils import *
import pandas as pd

the_data = pd.read_csv("test.csv", sep=",")
pd_slice = the_data[the_data["a"] < 3]
pd_slice_ex = the_data[(the_data["a"] < 3) & (the_data["a"] > 1)]

the_data.to_csv("test_a.csv", index=False) #write to csv

the_data.columns = ["col_a", "col_2", "col_3", "col_4"]

list_a = ["torhea", "class", "cis", "nlp"]
my_pd = pd.DataFrame()
for word in list_a:
    tmp = pd.DataFrame({"token": word, "length": len(word)}, index=[0])
    my_pd = pd.concat([my_pd, tmp], ignore_index=True)
    print (word)
    
my_pd["fun"] = [1, 2, 6, 8]

corpus_a = "the fish took my lure in the river but broke the line so i caught no fish"
#create a word frequency dictionary
wrd_freq = dict()
unique_tokens = set(corpus_a.split())
for ut in unique_tokens:
    wrd_freq[ut] = corpus_a.split().count(ut)
    
test = word_freq_fun(corpus_a)

f = open("ex.txt", "r")
tmp = f.read() #read reads in ALL the contents of the file
f.close()

f = open("ex.txt", "r")
tmp = f.readlines()
f.close()

#use this next version for LARGE files
f = open("ex.txt", "r")
tmp = f.readline()
print (tmp)
f.close()

the_path = "E:\Project\Python\pythonProject\NLP\data"
#file_name = "bassmasterfantasy.com_121742967000.txt"

#file_content = file_opener(the_path, file_name)

the_data = file_crawler(the_path)

pd_slice = the_data[the_data["label"] == "mathematics"]
str_cat = pd_slice["body"].str.cat(sep=" ")

test = word_freq_fun(str_cat)
#next week pick up here with word freq by topics

