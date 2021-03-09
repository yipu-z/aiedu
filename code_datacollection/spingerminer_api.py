# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 04:52:50 2021

@author: Jie Chen
"""
import requests
from bs4 import BeautifulSoup

# get issue links
ijcscl_url = "https://link.springer.com/journal/11412/volumes-and-issues"

journal_page = requests.get(ijcscl_url)
soup = BeautifulSoup(journal_page.text, 'html.parser')
links =  [a['href'] for a in soup.find_all('a')]
links = [l for l in links if '/journal/11412/volumes-and-issues/' in l]
links = ['https://link.springer.com' + l for l in links]

# get article links
alinks = []
for il in links:
    issue_page = requests.get(il)
    soup = BeautifulSoup(issue_page.text, 'html.parser')
    alinks.extend([a['href'] for a in soup.find_all('a')])

alinks = [l for l in alinks if 'https://link.springer.com/article/10.1007/' in l]
alinks = list(set(alinks))

sublinks = [l.replace("https://link.springer.com/article/10.1007/", "") for l in alinks]

# Send requests to each article pages
api_key = ''
apilink = ['http://api.springernature.com/meta/v2/json?q=doi:10.1007/'+ l + '&api_key=' + api_key for l in sublinks]
text = []
for al in apilink:
    req = requests.get(al)
    text.append(req.text)

# Write data into files
i = 0
for l in sublinks:
    with open(l+'.json', 'w', encoding='utf-8') as outfile:
        outfile.write(text[i])
        i += 1

# Write summary data into a file
with open('ijcscl_journal_api.json', 'w', encoding='utf-8') as outfile:
    outfile.write(text)