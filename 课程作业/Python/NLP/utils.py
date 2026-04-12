# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 07:47:48 2024

@author: pathouli
"""

#function
def hello_world():
    print ("Hello World")
    
def adder_test(a_in, b_in):
    tmp = a_in + b_in
    return tmp
    
def adder(a_in, b_in):
    try:
        tmp = a_in + b_in
        return tmp
    except:
        print ("Can't add a", type(a_in), "and", type(b_in), "together")
        pass
    
#Jaccardian measure function
def jaccard_fun(corpus_a_in, corpus_b_in):
    try:
        #tokenization
        corpus_a_token = set(corpus_a_in.split(" "))
        corpus_b_token = set(corpus_b_in.split(" "))
        
        #measure of similarity
        #length of intersection divided by the length of the union
        the_int = corpus_a_token.intersection(corpus_b_token)
        the_union = corpus_a_token.union(corpus_b_token)
        
        j_m = len(the_int) / len(the_union)
    except:
        print ("Ran into an error")
        pass
    return j_m

def clean_text(str_in):
    import re
    #corpus_test = "The cat#&@[]   chased the  dog!"
    corpus_clean = re.sub("[^A-Za-z]+", " ", str_in).strip().lower()
    return corpus_clean

def word_freq_fun(str_in):
    import collections
    wrd_freq_new = collections.Counter(str_in.split())
    return wrd_freq_new

def file_opener(path_in, file_in):
    f = open(path_in + file_in, "r", encoding="UTF8")
    tmp = f.read() #read reads in ALL the contents of the file
    f.close()
    tmp = clean_text(tmp)
    return tmp

def file_crawler(path_in):
    import pandas as pd
    my_data_t = pd.DataFrame()
    import os
    for root, dirs, files in os.walk(path_in, topdown=False):
       for name in files:
           try:
               tmp = file_opener(root + "/", name)
               if len(tmp) != 0:
                   tmp_df = pd.DataFrame(
                       {"body": tmp, "label": root.split("/")[-1:][0]}, index=[0])
                   my_data_t = pd.concat([my_data_t, tmp_df], ignore_index=True)
           except:
               print ("Issue with", root + "/", name)
               pass
    return my_data_t

def word_dict_fun(df_in, col_in):
    dictionary_t = dict()
    for topic in df_in.label.unique():
        tmp = df_in[df_in.label == topic]
        str_cat = tmp[col_in].str.cat(sep=" ")
        dictionary_t[topic] = word_freq_fun(str_cat)
    return dictionary_t

def rem_sw(str_in):
    from nltk.corpus import stopwords
    sw = stopwords.words("english")
    test_fix = list()
    for word in str_in.split():
        if word not in sw:
            test_fix.append(word)
    text_fix_fin = " ".join(test_fix)
    # text_fix_fin = " ".join(
    #     [word for word in test.split() if word not in sw])
    return text_fix_fin

def stem_fun(str_in):
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    sw_in = "porter"
    t_list = list()
    if sw_in == "porter":
        stem = PorterStemmer()
    else:
        lem = WordNetLemmatizer()
    for word in str_in.split():
        if sw_in == "porter":
            t_list.append(stem.stem(word))
        else:
            t_list.append(lem.lemmatize(word))
    t_list = " ".join(t_list)
    return t_list

def cos_fun(df_in, label_in):
    from sklearn.metrics.pairwise import cosine_similarity
    import pandas as pd
    cos_fun = pd.DataFrame(cosine_similarity(df_in, df_in))
    cos_fun.index = label_in
    cos_fun.columns = label_in
    
    metrics_dictionary = dict()
    for topic in set(cos_fun.index):
        tmp = cos_fun[cos_fun.index == topic]
        cos_fun_t = pd.DataFrame(cosine_similarity(tmp, tmp))
        metrics_t = cos_fun_t.mean(axis=1).mean()
        metrics_dictionary[topic] = metrics_t
    return cos_fun, metrics_dictionary

def t_form_fun(df_in, name_in, m_in, n_in, sw_in):
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    import pandas as pd
    
    if sw_in == "vec":
        vec = CountVectorizer(ngram_range=(m_in, n_in))
    else:
        vec = TfidfVectorizer(ngram_range=(m_in, n_in))
    
    xform_data_t = pd.DataFrame(vec.fit_transform(
        df_in[name_in]).toarray()) #carefull may run out of memory
    xform_data_t.columns = vec.get_feature_names_out()
    return xform_data_t

def pca_fun(df_in, var_in):
    from sklearn.decomposition import PCA
    pca = PCA(n_components=0.95)
    dim_data_t = pca.fit_transform(df_in)
    exp_var = sum(pca.explained_variance_ratio_)
    print ("Exp Var", exp_var)
    return dim_data_t

def write_pickle(obj_in, name, o_path):
    import pickle
    file = open(o_path + name + 'pk', 'wb')
    pickle.dump(obj_in, file)
    file.close()
    
def read_pickle(path_in, name):
    import pickle
    file = open(path_in + name + '.pk', 'rb')
    the_data_t = pickle.load(file)
    file.close()
    return the_data_t

def extract_embeddings_pre(df_in, out_path_i, name_in):
    #https://code.google.com/archive/p/word2vec/
    #https://pypi.org/project/gensim/
    #pip install gensim
    #name_in = 'models/word2vec_sample/pruned.word2vec.txt'
    import pandas as pd
    from nltk.data import find
    from gensim.models import KeyedVectors
    import pickle
    def get_score(var):
        import numpy as np
        tmp_arr = list()
        for word in var:
            try:
                tmp_arr.append(list(my_model_t.get_vector(word)))
            except:
                pass
        tmp_arr
        return np.mean(np.array(tmp_arr), axis=0)
    word2vec_sample = str(find(name_in))
    my_model_t = KeyedVectors.load_word2vec_format(
        word2vec_sample, binary=False)
    # word_dict = my_model.key_to_index
    tmp_out = df_in.str.split().apply(get_score)
    tmp_data = tmp_out.apply(pd.Series).fillna(0)
    pickle.dump(my_model_t, open(out_path_i + "embeddings.pkl", "wb"))
    pickle.dump(tmp_data, open(out_path_i + "embeddings_df.pkl", "wb" ))
    return tmp_data, my_model_t

def domain_train(df_in, path_in, name_in):
    #domain specific
    import pandas as pd
    import gensim
    def get_score(var):
        import numpy as np
        tmp_arr = list()
        for word in var:
            try:
                tmp_arr.append(list(model.wv.get_vector(word)))
            except:
                pass
        tmp_arr
        return np.mean(np.array(tmp_arr), axis=0)
    model = gensim.models.Word2Vec(df_in.str.split())
    model.save(path_in + 'body.embedding')
    #call up the model
    #load_model = gensim.models.Word2Vec.load('body.embedding')
    model.wv.similarity('fish','river')
    tmp_data = pd.DataFrame(df_in.str.split().apply(get_score))
    return tmp_data, model

def chi_fun(df_in, label_in, k_in, path_out, name_in):
    from sklearn.feature_selection import chi2
    from sklearn.feature_selection import SelectKBest
    import pandas as pd
    import pandas as pd
    feat_sel = SelectKBest(score_func=chi2, k=k_in)
    dim_data = pd.DataFrame(feat_sel.fit_transform(
        df_in, label_in))
    feat_index = feat_sel.get_support(indices=True)
    feature_names = df_in.columns[feat_index]
    dim_data.columns = feature_names
    sum_col = pd.DataFrame(dim_data.sum(axis=0))
    sum_col.index = dim_data.columns
    write_pickle(feat_sel, path_out, name_in)
    return dim_data, sum_col
