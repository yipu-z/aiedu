# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 00:47:42 2020

@author: Jie Chen
"""
import json
import pandas as pd
import numpy as np

jsonfile1 = "../data/AIED_20112020/iaied_conf_json_1120_summary.json"
jsonfile2 = "../data/JAIED_20132020/iaied_journal_json_1320_summary.json"

# Get all json data
jsondata = []
with open(jsonfile1) as file:
    jsondata.extend(json.loads(file.read()))
with open(jsonfile2) as file:
    jsondata.extend(json.loads(file.read()))

# Get publication year 2013-2020
tempjsondata = []
for singleinfo in jsondata:
    pubyear = int(singleinfo['data']['publication-year']) 
    if pubyear >= 2013 and pubyear <= 2020:
        tempjsondata.append(singleinfo)

jsondata = tempjsondata[:]

# Get keyword list
keyword = []
for singleinfo in jsondata:
    keyword.extend(singleinfo['data']['keywords'])
    
print("The total number of keywords from 2013-2020 for both journal and conference data is", len(keyword))

# Process keyword
tempkeyword = [w.lower() for w in keyword] # lower case
tempkeyword = list(set(tempkeyword))
df1 = pd.DataFrame()
df1['keyword'] = tempkeyword
print("The total number of unique keywords from 2013-2020 for both journal and conference data is", len(set(tempkeyword)))

"""
# match file
colnum = len(jsondata)
rownum = len(tempkeyword)
column_name = [singleinfo['name'] for singleinfo in jsondata]
df2 = pd.DataFrame(data = np.zeros((rownum, colnum)), columns=column_name, index = tempkeyword)
for singleinfo in jsondata:
    keywordinfo = singleinfo['data']['keywords']
    for kw in keywordinfo:
        for tkw in tempkeyword:
            if (kw.lower() == tkw):
                df2[singleinfo['name']][tkw] += 1
"""
"""
# Save to file
writer = pd.ExcelWriter('../data/keywords.xlsx')
df1.to_excel(writer, sheet_name="keyword-class", index=False)
df2.to_excel(writer, sheet_name="keyword-paper")
writer.save()
writer.close()
"""

import nltk
import spacy
from spacy import displacy
import en_core_web_sm
from nltk.stem import WordNetLemmatizer 
from nltk.stem import PorterStemmer 
from collections import Counter

nlp = en_core_web_sm.load()
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# Generate a dataframe for storing all types of NLP

df3 = pd.DataFrame(columns = ['keyword', 'ent_text', 'ent_label', 'noun_text', 'noun_postag', 'lemm', 'stem', 'common_word'])
df3['keyword'] = tempkeyword

# find NER, nouns, lemm, and stem

for k in tempkeyword:
    doc = nlp(k)
    if doc.ents:
        for X in doc.ents:
            df3.loc[df3['keyword'] == k, 'ent_text'] = X.text
            df3.loc[df3['keyword'] == k, 'ent_label'] = X.label_
    else:
        if nltk.pos_tag([k.split()[-1]])[0][1] == 'NN' or nltk.pos_tag([k.split()[-1]])[0][1] == 'NNS':
            df3.loc[df3['keyword'] == k, 'noun_text'] = nltk.pos_tag([k.split()[-1]])[0][0]
            df3.loc[df3['keyword'] == k, 'noun_postag'] = nltk.pos_tag([k.split()[-1]])[0][1]
    lemm = ' '.join([lemmatizer.lemmatize(w) for w in k.split()])
    stem = ' '.join([stemmer.stem(w) for w in k.split()])
    df3.loc[df3['keyword'] == k, 'lemm'] = lemm
    df3.loc[df3['keyword'] == k, 'stem'] = stem
wordset = []
for k in tempkeyword:
    for w in k.replace("-", " ").split():
        wordset.append(w)

# Count keyword frequency
wordset_counter = Counter(wordset)
wordset_large = Counter(el for el in wordset_counter.elements() if wordset_counter[el] >= 10)
great_words = [k for k,c in wordset_large.items()]
great_words.remove('in')
great_words.remove('to')
great_words.remove('of')

# Save keyword frequency to a dataframe and an excel
df_wordset = pd.DataFrame.from_dict(dict(wordset_counter), orient = 'index')
writer = pd.ExcelWriter('../data/wordset.xlsx')
df_wordset.to_excel(writer, index=True)
writer.save()
writer.close()

# Sort and find common keywords
for k in tempkeyword:
    for g in great_words:
        if g in k:
            df3.loc[df3['keyword'] == k, 'common_word'] = g

writer = pd.ExcelWriter('../data/Keyword Analysis1.xlsx')
df3.to_excel(writer)
writer.save()
writer.close()