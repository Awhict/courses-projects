# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 07:08:03 2024

@author: pathouli
"""

#from utils import hello_world, adder, jaccard_fun 
from utils import *

corpus_a = "the,cat,ran,up,the,hill,chasing,the,mouse"
corpus_b = "the dog chased the cat up the hill"

#tokenization
corpus_a_token = set(corpus_a.split(","))
corpus_b_token = set(corpus_b.split(" "))

#measure of similarity
#length of intersection divided by the length of the union
the_int = corpus_a_token.intersection(corpus_b_token)
the_union = corpus_a_token.union(corpus_b_token)

j_m = len(the_int) / len(the_union)

adder("hello", 456)

hello_world()

test_a = adder(3, 5)
test_b = adder(30, 521)

#test_b = adder(30, "World")
print ("Hello World")

test_b = adder(30, "World")

print ("Hello World")

test = jaccard_fun("the cat is cute", "heat wave in summer")
print (test)

print (clean_text("the cat%&&"))

#dictionary: key and value pair
dictionary_ex = dict()

dictionary_ex["key_a"] = 3.14
dictionary_ex["key_a"] = "patrick"
dictionary_ex["key_b"] = "beth"
dictionary_ex["key_c"] = "neoscholar"
dictionary_ex["key_d"] = [1, 2, 3, 4, 5]

the_keys = list(dictionary_ex.keys())
the_values = list(dictionary_ex.values())

#looping statements
token_a = ["patrick", "and", "beth", "teach", "class"]
for word in token_a:
    print (word)

for i in range(0, 10):
    print (i)
    
tmp = dict()
for word in token_a:
    tmp[word] = len(word)
    
my_int = 0
while my_int < 10:
    print (my_int)
    #my_int = my_int + 1
    my_int += 1


#control statements
a_int = 5
b_int = 10
c_int = 11

if a_int > b_int:
    print ("yeah!")
elif b_int == 12:
    print ("blah!")
elif c_int > b_int:
    print ("finally!")
elif 1 == 1:
    print ("did we get here?")

if a_int > b_int:
    print ("yeah!")
elif b_int == 12:
    print ("blah!")
elif c_int < b_int:
    print ("finally!")
elif 1 != 1:
    print ("did we get here?")
else:
    print ("whatever")


if a_int > b_int:
    print ("yeah!")
if b_int == 12:
    print ("blah!")
if c_int > b_int:
    print ("finally!")
if 1 == 1:
    print ("did we get here?")

print ("hello world")
#import pandas as pd
