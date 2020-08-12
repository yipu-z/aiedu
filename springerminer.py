# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 07:30:39 2020

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
    
    ris_url = 'https://link.springer.com' + url + '-references.ris'
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
    abstract = soup.select('#Abs1-content')[0].p.text
    
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
        paper_url = 'https://link.springer.com' + url
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
    print('Springer Paper Miner. \nIt is a program for mining Springer papers. This program will extract the references and paper information from all papers in a same journal, volume, and issue at one time. \n\nThe format of Springer link is \'https://link.springer.com/journal/[journal ID]/[volume]/[issue] \ne.g. International Journal of Artificial Intelligence in Education 2020, Volume 30, Issue 1. \nLink: https://link.springer.com/journal/40593/30/1\nJournal ID: 40593 \nVolume: 30 \nIssue: 1 \n\nPlease provide the journal ID, volume, and issue number. ')
    
    journal_id = input('Journal ID: ')
    volume = input('Volume: ')
    issue = input('Issue: ')
    
    journal_url = 'https://link.springer.com/journal/' + journal_id + '/' + volume + '/' + issue
    
    print('Mining papers and citations. The papers are on https://link.springer.com/journal/' + journal_id + '/' + volume + '/' + issue)
    
    journal_page = requests.get(journal_url)
    soup = BeautifulSoup(journal_page.text, 'html.parser')
    links = soup.select('#kb-nav--main div.toc ol li div h3 a')

    for a in links:
        href = a['href']
        save_json_springer(href)
        get_ris_springer(href)
    
    print('End of the program. \nAll successfully obtained ris files have stored in \"springer-citations\" folder. ')