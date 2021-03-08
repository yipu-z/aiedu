# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 06:59:52 2020

@author: Jie Chen

Description:
Format of processed data: bib
Table about the relation between title and keyword

"""
import bibtexparser
import csv 
import pandas as pd
import nltk
import spacy
from spacy import displacy
import en_core_web_sm
from nltk.stem import WordNetLemmatizer 
from nltk.stem import PorterStemmer 
from collections import Counter

"""
Parse bib data, load it to data frame and save
"""

path = '../lak data/lak.bib'

with open(path, 'rb') as bibtex_file:
    bibtex_str = bibtex_file.read()

bib_database = bibtexparser.loads(bibtex_str)

df = pd.DataFrame(bib_database.entries)
df.to_csv('lak.csv', index=False)

"""
Extract keywords from bib database
"""

tkdict = {}
for eachentry in bib_database.entries:
    title = eachentry['title']
    if 'keywords' in eachentry:
        karray = [k.strip() for k in eachentry['keywords'].split(',')]
        tkdict[title] = karray

"""
Generate table containing article title and keywords
"""

with open("../lak data/title-keyword.csv","w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["index","title","keyword"])
    count = 1
    for key, value in tkdict.items():
        for kw in value:
            writer.writerow([count, key, kw])
        count += 1

"""
Generate table counting keywords
"""

allkeywords = [value for value in tkdict.values()]
allkeywords = [kw for kwlist in allkeywords for kw in kwlist]

allkeywords_counter = Counter(allkeywords)
df2 = pd.DataFrame()
df2['keywords'] = allkeywords_counter.keys()
df2['count'] = allkeywords_counter.values()

writer = pd.ExcelWriter('../lak data/Keyword Count.xlsx')
df2.to_excel(writer)
writer.save()
writer.close()

"""
Process keyword
Methods: NER; noun; POS; Lemm; Stem; count
"""
tempkeyword = [w.lower() for w in allkeywords] # lower case
tempkeyword = list(set(tempkeyword))

df1 = pd.DataFrame()
df1['keyword'] = tempkeyword


nlp = en_core_web_sm.load()
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# Keyword process methods: NER; noun; POS; Lemm; Stem; count
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

# Remove stop words by obeservation
great_words.remove('for')
great_words.remove('of')

# wordset contain unique keywords of the database
df_wordset = pd.DataFrame.from_dict(dict(wordset_counter), orient = 'index')
writer = pd.ExcelWriter('../lak data/wordset.xlsx')
df_wordset.to_excel(writer, index=True)
writer.save()
writer.close()

for k in tempkeyword:
    for g in great_words:
        if g in k:
            df3.loc[df3['keyword'] == k, 'common_word'] = g

# Save to keywords analysis table
writer = pd.ExcelWriter('../lak data/Keyword Analysis1.xlsx')
df3.to_excel(writer)
writer.save()
writer.close()