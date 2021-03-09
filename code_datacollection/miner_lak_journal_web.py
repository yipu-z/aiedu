# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 04:33:56 2020

@author: Jie Chen


"""
import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import os

#journal -> eachjournal -> article

journal_url = "https://learning-analytics.info/index.php/JLA/issue/archive"

# Get LAK journal links

def get_journallinks_lak(journal_url):
    journal_page = requests.get(journal_url)
    soup = BeautifulSoup(journal_page.text, 'html.parser')
    alla = soup.find_all('a')
    links = []
    for a in alla:
        link = a.get('href')
        if link:
            if "learning-analytics.info/index.php/JLA/issue/view/" in link:
                links.append(link)
    links = list(set(links))
    return links

# Get each issue links

def get_eachjournallinks_lak(eachjournal_url):
    eachjournal_page = requests.get(eachjournal_url)
    soup = BeautifulSoup(eachjournal_page.text, 'html.parser')
    alla = soup.find_all('a')
    links = []    
    for a in alla:
        link = a.get('href')
        if link:
            if "https://learning-analytics.info/index.php/JLA/article/view/" in link:
                rule = r'.*view\/[0-9]+$'
                if re.match(rule, link):
                    links.append(link)
    links = list(set(links))
    return links

# Sample: https://learning-analytics.info/index.php/JLA/citationstylelanguage/download/bibtex?submissionId=6200&publicationId=10735
# Get each LAK article bibtext 
def get_eacharticle_bibtex_lak(eacharticle_url):
    eacharticle_page = requests.get(eacharticle_url)
    soup = BeautifulSoup(eacharticle_page.text, 'html.parser')
    alla = soup.find_all('a')
    for a in alla:
        link = a.get('href')
        if link:
            if "https://learning-analytics.info/index.php/JLA/citationstylelanguage/download/bibtex?" in link:
                return link
            else:
                continue

journallinks = get_journallinks_lak(journal_url)

article_url = []
for journallink in journallinks:
    article_url.extend(get_eachjournallinks_lak(journallink))

bibtex = []
for eacharticle_url in article_url:
    bibtex.append(get_eacharticle_bibtex_lak(eacharticle_url))

folderpath_citations = '../LAK data/bibtex/'
count = 0
for each_bibtex in bibtex:
    try:
        bib_file = urllib.request.urlretrieve(each_bibtex, folderpath_citations + str(count) + '.bib')
    except:
        print('[Error] Unable to retrieve ' + each_bibtex)
    else:
        print('[Success] ' + folderpath_citations + str(count) + '.bib saved')
    finally:
        count += 1

filenames = os.listdir(folderpath_citations)
bibpaths = [folderpath_citations + filename for filename in filenames]

file = open('lak_journal_web.bib', 'w', encoding='utf-8')

for bibpath in bibpaths:
    with open(bibpath, encoding='utf-8') as bib:
        file.write(bib.read())
    file.write('\n')
file.close()