# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 08:34:13 2020

@author: Jie Chen

Recommend by abstract. 
"""
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

conffile = "../data/AIED_20112020/iaied_conf_json_1120_summary.json"

# Get all json data
jsondata = []
with open(conffile) as file:
    jsondata.extend(json.loads(file.read()))

info = []
id = 0
for singleinfo in jsondata:
    info.append((id, singleinfo['data']['article-title'], singleinfo['data']['keywords'], singleinfo['data']['abstract']))
    id += 1

ds = pd.DataFrame(data = info, columns = ['id', 'article-title', 'keywords', 'abstract'])

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 4), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds['abstract'])

cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix) 
results = {}
for idx, row in ds.iterrows():
   similar_indices = cosine_similarities[idx].argsort()[:-100:-1] 
   similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices] 
   results[row['id']] = similar_items[1:]

def item(item_id):  
  return ds.loc[ds['id'] == item_id]['article-title'].tolist()[0].split(' - ')[0] 

# Just reads the results out of the dictionary.
def recommend(item_id, num):
    print("Recommending " + str(num) + " products similar to " + item(item_id) + "...")   
    print("-------")    
    recs = results[item_id][:num]   
    for rec in recs: 
       print("Recommended: " + item(rec[1]) + " (score:" +      str(rec[0]) + ")")

recommend(item_id=241, num=5)

def get_id(title):
    return ds.loc[ds['article-title'] == title]['id']