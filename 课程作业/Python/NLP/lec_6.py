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

#word_f_fun = word_dict_fun(the_data, "body")

#print (rem_sw("the cable guy is almost here"))

#the_data["body_sw"] = the_data.body.apply(rem_sw)

#word_f_fun_sw = word_dict_fun(the_data, "body_sw")

#the_data["body_sw_stem"] = the_data.body_sw.apply(stem_fun)

#write_pickle(the_data, "the_data", out_path)

the_data = read_pickle(out_path, "the_data")

#word_f_fun_stem = word_dict_fun(the_data, "body_sw_stem")

#xform_data = t_form_fun(the_data, "body_sw_stem", 1, 3, "vec")

# all_cos, ind_cos = cos_fun(xform_data, the_data.label)

#dim_data = pca_fun(xform_data, "0.95")

#chi_features, feat_imp = chi_fun(
#    xform_data, the_data.label, 100, "chi_fun", out_path)

emb_vec = extract_embeddings_pre(
    the_data.body, out_path, 'models/word2vec_sample/pruned.word2vec.txt')

emb_model = emb_vec[1]



#einstein + mechanics - relativity = ?Newton
king = emb_model.get_vector("king")
man = emb_model.get_vector("man")
woman = emb_model.get_vector("woman")

the_ans = king - man + woman

sim_tokens = emb_model.most_similar(the_ans)

sim_tokens = emb_model.most_similar("fish")

#newton = emb_model.get_vector("Newton")



#emd_dom = domain_train(the_data.body, out_path, "domain")


#chi-square, cosine_sim, embedding