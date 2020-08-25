# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 09:01:45 2020

@author: Jie Chen
"""
import csv
import json
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

def get_ngrams(sequence, n):
    
    # Generate n-gram list
    ngram_list = []
    
    if (n >= 1 and n <= len(sequence)): 
        
        # Add 'STOP' before processing sequence
        sequence_with_stop = sequence[:]
        sequence_with_stop.append('STOP')
        
        # index is the index of last word which should be stored in a tuple
        for index in range(len(sequence_with_stop)):
            
            ngram_tuple = ()
            # pointer points to the first element which should be stored in a tuple, 
            # then second element, and so on. pointer is no larger than index. 
            pointer = index - n + 1
            while pointer <= index:
                ngram_tuple += ('START', ) if pointer < 0 else (sequence_with_stop[pointer], )
                pointer += 1
            ngram_list.append(ngram_tuple)
            
    return ngram_list 

# Retrieve negative word list from file
# 'n' means will get the most common n words. 
def get_neg_words(filename, n):
    negwords = []
    with open(filename, newline='') as file:
        next(file)
        csvReader = csv.reader(file)
        count = 0
        for index, word, n_ in csvReader:
            negwords.append(word)
            count += 1
            if count == n:
                return negwords

negwords = get_neg_words("data/neg_wordlist.csv", 42)

# Get abstract corpus
with open("data/json_summary.json") as file:
    summary = json.load(file)
    data = [sublist['data'] for sublist in summary]
    abstract = [sublist['abstract'] for sublist in data]
corpus = abstract

# Get bigram in the format of tuple
bigrams_neg = []
for text in abstract:
    doc = nlp(text)
    token = [token.text for token in doc]
    bigrams = get_ngrams(token, 2)
    for tup in bigrams:
        for negw in negwords:
            if negw in tup:
                bigrams_neg.append(tup)

# Get trigram in the format of string for better output vision
trigrams_neg = []
bigrams_process = [bigrams_neg[i:i+2] for i in range(0,len(bigrams_neg),2)]
for tup1, tup2 in bigrams_process:
    trigrams_neg.append(tup1[0] + " " + tup1[1] + " " + tup2[1])

"""
with open('data/neg_trigrams.txt', 'w') as file:
    for grams in trigrams_neg:
        file.write(grams + '\n')
"""