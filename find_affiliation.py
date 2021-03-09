# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 03:42:20 2020

@author: Jie Chen
"""

"""
Extract all affiliations from IAIED data. I categorize affiliations by universities and non-universities*

*University refers to higher educational institution. 
"""

import json 
import csv
import pandas as pd
path1 = '../data/Revised Name Summary/iaied_journal_json_8920_summary (name revised).json'
path2 = '../data/Revised Name Summary/iaied_journal_json_1320_summary (name revised).json'
path3 = '../data/Revised Name Summary/iaied_conf_json_1120_summary (name revised).json'

path = path3
with open(path, "r") as file:
    jd = json.load(file)

uni = {}
nonuni = {}

for d in jd:
    data = d['data']
    author = data['author']
    aff = []
    for eachauth in author:
        if 'affiliation' in eachauth:
            if isinstance(eachauth['affiliation'], str):
                aff.append(eachauth['affiliation'])
            elif isinstance(eachauth['affiliation'], list):
                for eachaff in eachauth['affiliation']:
                    aff.append(eachaff)
                    
    # the tags are filters for the educational institutions (universities)
    uni_tag = ['universi', 'polytechnic institute', 'advanced institute', 'college', 'polytechnique']
    
    isuni = False
    for tag in uni_tag:
        if tag in " ".join(aff).lower():
            isuni = True

    if isuni:
        uni[data['article-title']] = list(set(aff))
    else:
        nonuni[data['article-title']] = list(set(aff))

with open('conf1120_nonuni.json', 'w') as f:
    json.dump(nonuni, f)

with open('conf1120_uni.json', 'w') as f:
    json.dump(uni, f)