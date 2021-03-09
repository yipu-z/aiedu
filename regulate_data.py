# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 08:05:09 2020

@author: Jie Chen
"""

import json
import numpy as np
import pandas as pd
import re
import unicodedata

path1 = '../data/JAIED_19892020_web/iaied_journal_json_8920_summary.json'
path2 = '../data/JAIED_20132020/iaied_journal_json_1320_summary.json'
path3 = '../data/AIED_20112020/iaied_conf_json_1120_summary.json'

namelist = '../data/Revised Name Summary/Name Revised List.csv'

with open(path1, "r") as file:
    jd1 = json.load(file)
    
with open(path2, "r") as file:
    jd2 = json.load(file)
    
with open(path3, "r") as file:
    jd3 = json.load(file)
    
data1 = [d['data'] for d in jd1]
data2 = [d['data'] for d in jd2]
data3 = [d['data'] for d in jd3]

def test_ifislist(path):
    with open(path, "r") as file:
        jd = json.load(file)
    data = [d['data'] for d in jd]
    auth = [d['author'] for d in data]
    for d in auth:
        if not isinstance(d, list):
            print(d)

#test_ifislist('../data/AIED_20112020/iaied_conf_json_summary.json')

path = path3
with open(path, "r") as file:
    jd = json.load(file)
data = [d['data'] for d in jd]
auth = [d['author'] for d in data]
name = [auth_individual['author-name'] for auth_eachpaper in auth for auth_individual in auth_eachpaper]
name_lower = [n.lower() for n in name]
name_unique = sorted(list(set(name_lower)))

def check_lastname(fullnamelist):
    # Get last name list
    lastnamelist = [fullname.split()[-1] for fullname in fullnamelist]
    # Get unique last name list
    lastnamelist_unique = sorted(list(set(lastnamelist)))
    # Copy the lists for temporary use
    lastnamelist_temp = lastnamelist[:]
    lastnamelist_unique_temp = lastnamelist_unique[:]
    # Want to get last names which are repetitive, for finding out if there is any same person using different names
    # Assumption is that each person won't have different last name, but is possible to have different first names
    # The following code aims to pop the unique names, thus the duplicated names will remain in the list
    for lastname in lastnamelist:
        if lastname in lastnamelist_unique_temp:
            # If a unique name is detected, then remove it from list
            # and also remove it from temp unique name list, so that it will not be detected for a second time
            lastnamelist_unique_temp.remove(lastname)
            lastnamelist_temp.remove(lastname)
    # Copy the temporary list, then get unique list
    lastnamelist_duplicate = lastnamelist_temp[:]
    lastnamelist_duplicate = list(set(lastnamelist_duplicate))
    # If last name appears on this list, then possible that some people use different names
    checkname = []
    for ln in lastnamelist_duplicate:
        for fn in fullnamelist:
            if ln == fn.split()[-1]:
                checkname.append(fn)
    return checkname
   
checkname = check_lastname(name_unique)

with open(namelist, 'r') as nlfile:
    names = nlfile.readlines()
names = [n.strip() for n in names]
names = [n for n in names if n]
nameli = [(n.split(',')[0].strip(), n.split(',')[1].strip()) for n in names]
namedict = {}
for n in names:
    namedict[n.split(',')[0].strip()] = n.split(',')[1].strip()

def substitute_names(path):
    with open(path, "r") as file:
        text = file.read()
        text = unicodedata.normalize("NFKD", text)
    for n in nameli:
        text = re.sub(n[0], n[1], text)
    return text

text1 = substitute_names(path1)
text2 = substitute_names(path2)
text3 = substitute_names(path3)

datain_8919 = json.loads(text1)
datain_8919 = [d for d in datain_8919 if d['data']['publication-year'] != '2020']
datain_20 = json.loads(text2)
datain_20 = [d for d in datain_20 if d['data']['publication-year'] == '2020']
datain = datain_8919 + datain_20
datain_json = json.dumps(datain)

datain_all = json.loads(text)
auth_all = [d['data']['author'] for d in datain_all]
name_all = [auth_individual['author-name'] for auth_eachpaper in auth_all for auth_individual in auth_eachpaper]

"""
datain = json.loads(text2)
datain = [d['data'] for d in datain]
authin = [d['author'] for d in datain]
namein = [auth_individual['author-name'] for auth_eachpaper in authin for auth_individual in auth_eachpaper]
"""

"""
tempnamein = namein[:]
for i in range(0, len(namein)):
    if namein[i] in namedict:
        print('Change', namein[i], 'to', namedict[namein[i]])
        tempnamein[i] = namedict[namein[i]]
"""





















