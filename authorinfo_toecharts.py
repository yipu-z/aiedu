# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 09:02:08 2020

@author: Jie Chen

Description: 
    Generate data format which fits Echarts. 
    Sample: https://echarts.apache.org/examples/en/editor.html?c=graph-webkit-dep
    Format sample: http://static.popodv.com/data/attr/webkit-dep.json
"""

import csv
import json

links = []
with open("data/relation.csv", "r") as file:
    csvReader = csv.DictReader(file)
    for rows in csvReader:
        source = rows['source']
        target = rows['target']
        links.append({"source" : int(source), "target" : int(target)})

nodes = []
with open("data/author_table.csv", "r") as file:
    csvReader = csv.DictReader(file)
    for rows in csvReader:
        name = rows['name']
        nodes.append({"name" : name, "value" : 1, "category" : 0})
        
webkitDep = {
    "type" : "force",
    "categories" : [
        {
            "name" : "author",
            "keyword" : {}}],
    "nodes" : nodes, 
    "links" : links}

with open("data/echarts.json", "w") as outfile:
    json.dump(webkitDep, outfile)