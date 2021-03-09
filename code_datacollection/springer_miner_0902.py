# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 07:53:01 2020

@author: Jie Chen
"""

# Springer Paper Miner
import urllib.request
import os
import re
import requests
from bs4 import BeautifulSoup
import json

folderpath_citations = './springer-citations/'
if not os.path.exists(folderpath_citations):
    os.mkdir(folderpath_citations)

folderpath_paper = './iaied/'
if not os.path.exists(folderpath_paper):
    os.mkdir(folderpath_paper)
        
def get_ris_springer(url):
    
    ris_url = url + '-references.ris'
    rule = r'\/([^\/]*ris)$'
    ris_filename = re.findall(rule, ris_url)[0]
    try:
        ris_file = urllib.request.urlretrieve(ris_url, folderpath_citations + ris_filename)
    except:
        print('[Error] Unable to retrieve ' + ris_url)
    else:
        print('[Success] ' + ris_filename + ' saved')

def get_json_springer(paper_url):
    
    page = requests.get(paper_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    article_title = soup.find(attrs={"data-test":"article-title"}).text
    author_name = [name_html.text for name_html in soup.find_all(attrs={"data-test":"author-name"})]
    author_affiliation = [aff_html.meta['content'] for aff_html in soup.find_all(attrs={"itemprop":"affiliation"})]
    author_address = [addr_html['content'] for addr_html in soup.find_all(attrs={"itemprop":"address"})]
    author = []
    if len(author_name) == len(author_affiliation) and len(author_name) == len(author_address): 
        count = len(author_name)
        for i in range(0,count):
            author.append({'author-name' : author_name[i], 'affiliation' : author_affiliation[i], 'address' : author_address[i]})
        status = True
    else:
        status = False
        print("[Warning] " + paper_url + " The numbers of authors and affliations do not match. Will store author name only. ")
        count = len(author_name)
        for i in range(0,count):
            author.append({'author-name' : author_name[i]})
    journal_title = soup.find(attrs={"data-test":"journal-title"}).text
    journal_volume = "".join(soup.find(attrs={"data-test":"journal-volume"}).text.split())
    pageStart = soup.find(attrs={"itemprop":"pageStart"}).text
    pageEnd = soup.find(attrs={"itemprop":"pageEnd"}).text
    publication_year = soup.find(attrs={"data-test":"article-publication-year"}).text
    keywords = [word_html.text for word_html in soup.find_all(attrs={"itemprop":"about"})]
    citation = soup.find(attrs={"class":"c-bibliographic-information__citation"}).text
    try:
        abstract = soup.select('#Abs1-content')[0].p.text
    except:
        abstract = ""
    data = {
        'article-title' : article_title, 
        'author' : author,
        'journal-title' : journal_title,
        'journal-volume' : journal_volume,
        'pageStart' : pageStart,
        'pageEnd' : pageEnd,
        'publication-year' : publication_year,
        'keywords' : keywords,
        'citation' : citation,
        'abstract' : abstract
        }
    
    jsondata = json.dumps(data)
    return jsondata, status


def save_json_springer(url):
    
    rule = r'\/([^\/]*)$'
    data_filename = re.findall(rule, url)[0]
    
    filepath = folderpath_paper + data_filename + '.json'
    if os.path.exists(filepath):
        print(filepath + ' already exists. Will not override.')
    else: 
        txt = open(filepath, 'w')
        paper_url = url
        try:
            jsondata, status = get_json_springer(paper_url)
            
            if status == False:
                txt.close()
                os.remove(filepath)
                filepath = folderpath_paper + data_filename + '-doublecheck.json'
                txt = open(filepath, 'w')
            txt.write(jsondata)
        except:
            print('[Error] ' + paper_url + ' not saved.')
            txt.close()
            os.remove(filepath)
        else:
            print('[Success] ' + paper_url + ' saved as ' + filepath)

def main():
  
    journal_url_list = ['https://link.springer.com/journal/40593/23/1', 'https://link.springer.com/journal/40593/24/1', 'https://link.springer.com/journal/40593/24/2', 'https://link.springer.com/journal/40593/24/3', 'https://link.springer.com/journal/40593/24/4']
    
    for journal_url in journal_url_list:
        journal_page = requests.get(journal_url)
        soup = BeautifulSoup(journal_page.text, 'html.parser')
        links = soup.find_all(attrs={"data-track-action":"clicked article"})
    
        for a in links:
            href = a['href']
            save_json_springer(href)
            get_ris_springer(href)    

    print('End of the program. \nAll successfully obtained ris files have stored in \"springer-citations\" folder. ')
