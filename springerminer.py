# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 07:30:39 2020

@author: Jie Chen
"""

# Springer Reference Miner
import urllib.request
import os
import re
import requests
from bs4 import BeautifulSoup

def get_ris_springer(url):
    #article_page = requests.get(url)
    #soup = BeautifulSoup(article_page.text, 'html.parser')
    #ris_html = soup.find('a', attrs = {'data-track-action':'download citation references'})['href']
    #ris_url = 'https://link.springer.com' + ris_html
    
    ris_url = 'https://link.springer.com' + url + '-references.ris'
    rule = r'\/([^\/]*ris)$'
    ris_filename = re.findall(rule, ris_url)[0]
    try:
        ris_file = urllib.request.urlretrieve(ris_url, folderpath + ris_filename)
    except:
        print('[Error] Unable to retrieve ' + ris_url)    
    else:
        print('[Success] ' + ris_filename + ' saved')

print('Springer Reference Miner. \nIt is a program for mining references of Springer papers. This program will extract the references from all papers in a same journal, volume, and issue at one time. \n\nThe format of Springer link is \'https://link.springer.com/journal/[journal ID]/[volume]/[issue] \ne.g. International Journal of Artificial Intelligence in Education 2020, Volume 30, Issue 1. \nLink: https://link.springer.com/journal/40593/30/1\nJournal ID: 40593 \nVolume: 30 \nIssue: 1 \n\nPlease provide the journal ID, volume, and issue number. ')

journal_id = input('Journal ID: ')
volume = input('Volume: ')
issue = input('Issue: ')

journal_url = 'https://link.springer.com/journal/' + journal_id + '/' + volume + '/' + issue

print('Mining references of the papers. The papers are on https://link.springer.com/journal/' + journal_id + '/' + volume + '/' + issue)

journal_page = requests.get(journal_url)
soup = BeautifulSoup(journal_page.text, 'html.parser')
links = soup.select('#kb-nav--main div.toc ol li div h3 a')

folderpath = './springer-citations/'
if not os.path.exists(folderpath):
    os.mkdir(folderpath)

for a in links:
    #article_url = 'https://link.springer.com' + a['href']
    get_ris_springer(a['href'])

print('End of the program. \nAll successfully obtained ris files have stored in \"springer-citations\" folder. ')