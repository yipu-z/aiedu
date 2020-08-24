# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 12:40:22 2020

@author: Jie Chen

Tutorials:
    https://networkx.github.io/documentation/stable/reference/drawing.html#module-networkx.drawing.nx_pylab
"""

import json
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import itertools

# load json file
path = "data/json_summary.json"

jd = ""
with open(path, "r") as file:
    jd = json.load(file)

if jd != "":
    jd_data = [d['data'] for d in jd]
    jd_auth = [a['author'] for a in jd_data]
    
    # get author names within institutions
    jd_auth_name = []
    for sublist in jd_auth:
        if len(sublist) == 1:
            jd_auth_name.append([sublist[0]['author-name']])
        else:
            namelist = []
            for item in sublist:
                namelist.append(item['author-name'])
            jd_auth_name.append(namelist)
    
    # get unique author names regardless of institutions
    jd_auth_name_unique = []
    for sublist in jd_auth_name:
        if len(sublist) == 1:
            jd_auth_name_unique.extend(sublist)
        else:
            for item in sublist:
                jd_auth_name_unique.append(item)
    jd_auth_name_unique = sorted(list(set(jd_auth_name_unique)))
    
    # get relations of authors
    all_relation = []
    
    for sublist in jd_auth_name:
        if len(sublist) > 1:
            relation = sorted(list(itertools.combinations(sublist, 2)))
            all_relation.extend(relation)
    
    # number of distinct authors
    count = len(jd_auth_name_unique)
    
    # asymmetric matrix, one relation between authors will only count once
    pdmatrix = pd.DataFrame(data = np.zeros((count, count)), columns=jd_auth_name_unique, index = jd_auth_name_unique)
    for t in all_relation:
        pdmatrix[t[0]][t[1]] += 1
    
    # plot graph (currently unweighted)
    # using matplot to show the graph
    plt.figure(figsize=(40, 40))

    G_weighted = nx.Graph()
    
    relation_table = pdmatrix.reset_index().melt(id_vars='index').query('value > 0')
    for index, variable, value in relation_table[['index', 'variable', 'value']].itertuples(index=False):
        G_weighted.add_edge(index, variable, weight = value)
    
    #pos = nx.kamada_kawai_layout(G_weighted)
    nx.draw_networkx(G_weighted, node_size=20, font_size=10, font_family='sans-serif')

    plt.show()
    
    # generate symmetric matrix, save it to sna_table
    relation_matrix = pd.DataFrame(data = np.zeros((count, count)), columns=jd_auth_name_unique, index = jd_auth_name_unique)
    for t in all_relation:
        relation_matrix[t[0]][t[1]] += 1
        relation_matrix[t[1]][t[0]] += 1
    relation_matrix.to_csv("data/sna_table.csv")