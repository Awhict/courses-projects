# -*- coding: utf-8 -*-
"""
Multi-line comment
Created on Sat Mar  9 06:44:11 2024

@author: pathouli

Lecture 1
"""

#single line comment

print ("Hello World!")
print ("Hello Students!")
print ("Hello Universe!")

print ("Hello Universe!", "Saturday", "March", 5)

my_string = "neoschool"

len(my_string)

type(my_string)

#data types: string, integer, float, boolean

my_int = 10 #data type integer

my_float = 3.14 #data type float

my_bool_true = True
my_bool_false = False

#string

my_string_a = "patrick"
my_string_b = "houlihan"

#concatenation
str_concat = my_string_a + " " + my_string_b

#repeat
str_mult = my_string_a*4

test_a = my_string_a + my_int

my_int_str = str(my_int)

test_b = my_string_a + my_int_str

str_a = "patrick"
str_a_int = int(str_a)

str_b = "2024"
str_b_int = int(str_b)

type(str_b)

#data structures

#lists
#my_list = [] #infer
my_list = list() #explicit

my_list.append("saturday")
my_list.append("sunday")
my_list.append("saturday")
my_list.append("friday")

len(my_list)
#index starts at 0

my_list[3]

my_list[-1:] #last entry to any list

my_list[:2] #firts 2 entries

#reverse order of a list
my_list_rev = my_list[::-1]

#copying a list
my_copy = my_list_rev

my_list_rev.append("tuesday")

#true copy and indepedant
true_copy = my_list_rev.copy()

my_list_rev.append("thursday")

my_list_a = [1, 2, 3]
my_list_b = [4, 6, 8]

my_list_a.append(my_list_b)

my_list_a_t = [1, 2, 3]
my_list_b_t = [4, 6, 8]

my_list_a_t.extend(my_list_b_t)

#set - only 1 specific data type value allowed
my_set = set()
my_set.add("friday")
my_set.add("saturday")
my_set.add("sunday")
my_set.add("friday")

my_set.add("Friday")

str_test = "Friday"
str_test_a = "friday"

#equivalency test ==
str_test.lower() == str_test_a

my_set_a = {"20-24", "audi", "fish", "montana"}
my_set_b = {"55+", "audi", "swim", "nyc"}

#set logic
#union

union_t = my_set_b.union(my_set_a)

#intersection
intersection_t = my_set_b.intersection(my_set_a)

#what does one set have that another doesnt?
set_diff = my_set_b.difference(my_set_a)

#what attributes are NOT shared
sym_diff = my_set_a.symmetric_difference(my_set_b)

#sets stage for jaccardian measure next week
