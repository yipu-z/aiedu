# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 04:17:58 2020

@author: Jie Chen
"""
import os
import json

path = "../../data/JAIED_20132020/iaied_journal_json_20-3_/"

result = []
for file in os.listdir(path):
    with open(path + file, "r") as infile:
        name = file
        data = json.load(infile)
        result.append({"name" : name, "data" : data})
with open("../../data/JAIED_20132020/iaied_journal_json_1320_subsummary.json", "w") as outfile:
    json.dump(result, outfile)
