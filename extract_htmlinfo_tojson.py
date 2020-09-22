# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 12:10:34 2020

@author: Jie Chen
"""
from bs4 import BeautifulSoup
import json
import unicodedata
import re 
import os
from os import listdir

def get_json_springer_conf(filename):
    with open(filename, encoding='utf8') as file:
        html_text = unicodedata.normalize("NFKD", file.read())
    
    soup = BeautifulSoup(html_text, 'html.parser')
    
    article_title = soup.find(attrs={"class":"ChapterTitle"}).text
    
    author_name = [html.text for html in soup.find_all(attrs={"class":"authors-affiliations__name"})]
    
    try:
        if soup.find(attrs={"class":"test-affiliations"}):
            author_affiliation_index = []
            for html in soup.find_all(attrs={"class":"authors-affiliations__indexes"}):
                each_auth_index = []
                for li in html:
                    each_auth_index.append(li.text)
                author_affiliation_index.append(each_auth_index)
            author_affiliations = [html for html in soup.find(attrs={"class":"test-affiliations"})]
            author_affiliations_dict = {}
            for aff in author_affiliations:
                count = aff.find(attrs={"class":"affiliation__count"}).text
                count = re.findall(r'\d+', count)[0]
                name = aff.find(attrs={"class":"affiliation__name"}).text
                author_affiliations_dict[count] = name
        
            author_affiliation_array = []
            for i in author_affiliation_index:
                if len(i) == 1:
                    for j in i:
                        author_affiliation_array.append(author_affiliations_dict[j])
                else:
                    temp = []
                    for j in i:
                        temp.append(author_affiliations_dict[j])
                    author_affiliation_array.append(temp)
        
            author = []
            count = len(author_name)
            for i in range(0,count):
                author.append({'author-name' : author_name[i], 'affiliation' : author_affiliation_array[i]})
    except:
        author = []
        count = len(author_name)
        for i in range(0,count):
            author.append({'author-name' : author_name[i]})

    conf_title = soup.find(attrs={"data-test":"ConfSeriesName"}).text.lstrip()
    conf_acronym = soup.find(attrs={"data-test":"ConferenceAcronym"}).text
    book_title = soup.find(attrs={"class":"BookTitle"}).text
    page_num_info =  " ".join(soup.find(attrs={"class":"page-numbers-info"}).text.split())
    keywords = [word_html.text.rstrip() for word_html in soup.find_all(attrs={"class":"Keyword"})]
    citation = soup.find(attrs={"id":"citethis-text"}).text
    try:
        abstract = soup.select('.Abstract')[0].p.text
    except:
        abstract = ""
    
    data = {
        'article-title' : article_title, 
        'author' : author,
        'conf-title' : conf_title,
        'conf-acronym' : conf_acronym,
        'book-title' : book_title,
        'page-info' : page_num_info,
        'keywords' : keywords,
        'citation' : citation,
        'abstract' : abstract
        }
    
    jsondata = json.dumps(data)
    
    return jsondata

def save_json_springer(filename_input, filename_output):
    
    status = False
    message = ""
    if os.path.exists(filename_output):
        print(filename_output + ' already exists. Will not override.')
        status = True
    else: 
        txt = open(filename_output, 'w')
        try:
            jsondata = get_json_springer_conf(filename_input)
            txt.write(jsondata)
        except:
            print('[Error] ' + filename_output + ' not saved.')
            txt.close()
            os.remove(filename_output)
            message = filename_input
        else:
            print('[Success] ' + filename_output + ' saved.')
            txt.close()
            status = True
    return status, message

folder_path_input = '../data/iaied_conf_html_1120'
folder_path_output = '../data/iaied_conf_json_1120'

if not os.path.exists(folder_path_output):
    os.mkdir(folder_path_output)

filename_input_array = [folder_path_input + '/' + f for f in listdir(folder_path_input)]

filename_output_array = [(folder_path_output + '/' + f).replace('.html', '.json') for f in listdir(folder_path_input)]

error = []

count = len(filename_input_array)
for i in range(0, count):
    status, message = save_json_springer(filename_input_array[i], filename_output_array[i])
    if status == False:
        error.append(message + '\n')

with open('../data/error_file.txt', 'w') as file:
    file.writelines(error)
