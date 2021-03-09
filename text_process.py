# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 08:17:58 2020

@author: Jie Chen
"""

import os
import re
import json
from collections import Counter

textpath1 = '../data/AIED_20112020/iaied_conf_text_1120/'
textpath2 = '../data/JAIED_20132020/iaied_journal_text_1320/'
absfile1 = '../data/AIED_20112020/iaied_conf_json_1120_summary.json'
absfile2 = '../data/JAIED_20132020/iaied_journal_json_1320_summary.json'


def get_all_text_from_folder(path):
    textlist = []
    for file in os.listdir(path):
        with open(path + file, encoding='utf8') as infile:
            textlist.append(infile.read())
    return textlist

def get_all_abstract_fromfile(filename, path):
    filenamelist = os.listdir(path)
    
    with open(filename, encoding = 'utf8') as infile:
        json.load

def findfilename_bykeyword_fromfolder(keyword, path):
    filenamelist = []
    for file in os.listdir(path):
        with open(path + file, encoding='utf8') as infile:
            text = infile.read()
            if keyword in text:
                filenamelist.append(file)
    return filenamelist

#print(findfilename_bykeyword_fromfolder("Sim", textpath1))

textlist = []
textlist.extend(get_all_text_from_folder(textpath1))
textlist.extend(get_all_text_from_folder(textpath2))

# Global virable
subwords = ["Introduction", "Work", "Conclusions", "Conclusion", "Discussion", "Data", "Implementation", "Study", "Methods", "Method", "Design", "Models", "Model", "Systems", "System", "Procedure", "Performance", "Evaluation","Approach", "Features", "Questions", "Feedback", "Framework", "Experiments", "Research", "Assessment", "Contributions", "Motivation", "Development", "Participants", "Context", "Architecture", "Environments", "Processing", "Limitations", "Collection", "Overview", "Extraction", "Experiment", "Group", "Generation", "Analysis", "Results", "Result", "Learning", "Review", "Environment", "Background", "Intervention", "Annotation", "Description", "Criteria", "Setting", "Studies", "Tutor"]

def find_adhesive_words(text):
    pattern = re.compile('\s[A-Z][a-z]+[A-Z][a-z]+\s')
    words = pattern.findall(text)
    firstword = []
    for w in words:
        firstword.append(re.compile('[A-Z][a-z]+').findall(w)[0])
    return firstword

def find_adhesive_words_unique(text):
    pattern = re.compile('\s[A-Z][a-z]+[A-Z][a-z]+\s')
    words = pattern.findall(text)
    firstword = []
    for w in words:
        firstword.append(re.compile('[A-Z][a-z]+').findall(w)[0])
    firstword = list(set(firstword))
    return firstword

def find_sentence_byword_intext(word, text):
    result = []
    sentencelist = text.split('. ')
    for sentence in sentencelist:
        if word in sentence:
            result.append(sentence)
    if result:
        return result
    else:
        return None

def find_sentence_byword(word, textlist):
    sentence = []
    for text in textlist:
        s = find_sentence_byword_intext(word, text)
        if s: sentence.extend(s)
    if sentence: return sentence
    else: return None

def find_word_byprefix_intext(pre, text):
    pattern = re.compile(pre + '[A-Z][a-z]+\s')
    words = pattern.findall(text)
    if words:
        words = list(set(words))
        return words
    else: return None

def find_word_byprefix(pre, textlist):
    word = []
    for text in textlist:
        w = find_word_byprefix_intext(pre, text)
        if w: word.extend(w)
    if word: return word
    else: return None

def text_list_preprocess(textlist):
    # Divide presumable adjesove words
    adhesive_words = []
    for text in textlist:
        adhesive_words.extend(find_adhesive_words(text))    
    #print(Counter(adhesive_words).most_common(50))
    for i in range(0, len(textlist)):
        for w in subwords:
            textlist[i] = textlist[i].replace(w, w+' ')
    # Divide presumable adjesove words
    adhesive_words = []
    for text in textlist:
        adhesive_words.extend(find_adhesive_words_unique(text))    
    print(Counter(adhesive_words).most_common(50))
    return textlist

textlist = text_list_preprocess(textlist)
sentence = find_word_byprefix('Rapid', textlist)
#print(find_sentence_byword('Mc', textlist))
