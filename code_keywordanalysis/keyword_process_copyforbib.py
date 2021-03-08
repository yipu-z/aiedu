# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 10:38:57 2021

@author: Jie Chen
"""
import bibtexparser
import pandas as pd

path = "../../other data/lats_conference/LatS_conference_acm.bib"

with open(path, 'rb') as bibtex_file:
    bibtex_str = bibtex_file.read()

bib_database = bibtexparser.loads(bibtex_str)

tkdict = {}
for eachentry in bib_database.entries:
    title = eachentry['title']
    if 'keywords' in eachentry:
        karray = [k.strip() for k in eachentry['keywords'].split(',')]
        tkdict[title] = karray

allkeywords = [value for value in tkdict.values()]
allkeywords = [kw for kwlist in allkeywords for kw in kwlist]

# Process keyword
tempkeyword = [w.lower() for w in allkeywords] # lower case
tempkeyword = list(set(tempkeyword))
df1 = pd.DataFrame()
df1['keyword'] = tempkeyword
print(len(set(tempkeyword)))

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

df3 = pd.DataFrame(columns = ['keyword', 'ent_text', 'ent_label', 'noun_text', 'noun_postag', 'lemm', 'stem', 'common_word'])
df3['keyword'] = tempkeyword

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

wordset_counter = Counter(wordset)
wordset_large = Counter(el for el in wordset_counter.elements() if wordset_counter[el] >= 10)
great_words = [k for k,c in wordset_large.items()]
great_words.remove('and')
great_words.remove('to')
great_words.remove('for')
great_words.remove('of')

df_wordset = pd.DataFrame.from_dict(dict(wordset_counter), orient = 'index')
writer = pd.ExcelWriter('../../other data/lats_conference/lats_wordset.xlsx')
df_wordset.to_excel(writer, index=True)
writer.save()
writer.close()

for k in tempkeyword:
    for g in great_words:
        if g in k:
            df3.loc[df3['keyword'] == k, 'common_word'] = g

writer = pd.ExcelWriter('../../other data/lats_conference/lats_keyword_analysis.xlsx')
df3.to_excel(writer)
writer.save()
writer.close()