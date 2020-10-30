# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 03:05:50 2020

@author: Jie Chen
"""
import json
import pandas as pd
from collections import defaultdict
from collections import Counter

with open("data/json_summary.json") as file:
    summary = json.load(file)
    data = [sublist['data'] for sublist in summary]
    keywords = [sublist['keywords'] for sublist in data]
    keywords_all = [keyword for sublist in keywords for keyword in sublist]
    c = Counter(keywords_all)
    d = dict(c)
    df = pd.DataFrame(columns = ['Key', 'Value'])
    for i, j in d.items():
        df = df.append([{'Key' : i, 'Value' : j}], ignore_index = True)
    df.to_csv('data/keyword_dict.csv')
    common = c.most_common(10)