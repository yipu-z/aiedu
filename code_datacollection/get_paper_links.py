# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 04:22:57 2020

@author: Jie Chen
"""
import re
import requests
from bs4 import BeautifulSoup

# Get journal paper links

def get_journal_paper_links():
    page = requests.get("https://link.springer.com/journal/40593/volumes-and-issues")
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all(class_="c-list-group__item")
    links = ["https://link.springer.com" + l.a['href'] for l in links]
    
    all_paper_links = []
    for l in links:
        page = requests.get(l)
        soup = BeautifulSoup(page.text, 'html.parser')
        paper_links = [a['href'] for a in soup.find_all(attrs={"itemprop":"url"})]
        all_paper_links.extend(paper_links)
        
    store_paper_links = [l + "\n" for l in all_paper_links]
    with open('journal-paper-links.txt', 'w') as file:
        file.writelines(store_paper_links)

# Conference paper links

def get_conference_paper_links():
    paper_links = []
    book_url = ['https://link.springer.com/book/10.1007/978-3-030-52237-7',
                'https://link.springer.com/book/10.1007/978-3-030-52240-7',
                'https://link.springer.com/book/10.1007/978-3-030-23204-7',
                'https://link.springer.com/book/10.1007/978-3-030-23207-8',
                'https://link.springer.com/book/10.1007/978-3-319-93843-1',
                'https://link.springer.com/book/10.1007/978-3-319-93846-2',
                'https://link.springer.com/book/10.1007/978-3-319-61425-0',
                'https://link.springer.com/book/10.1007/978-3-319-19773-9',
                'https://link.springer.com/book/10.1007/978-3-642-39112-5',
                'https://link.springer.com/book/10.1007/978-3-642-21869-9']
    
    chapter_url_prefix = ['https://link.springer.com/chapter/10.1007/978-3-030-52237-7_',
                          'https://link.springer.com/chapter/10.1007/978-3-030-52240-7_',
                          'https://link.springer.com/chapter/10.1007/978-3-030-23204-7_', 
                          'https://link.springer.com/chapter/10.1007/978-3-030-23207-8_', 
                          'https://link.springer.com/chapter/10.1007/978-3-319-93843-1_', 
                          'https://link.springer.com/chapter/10.1007/978-3-319-93846-2_',
                          'https://link.springer.com/chapter/10.1007/978-3-319-61425-0_',
                          'https://link.springer.com/chapter/10.1007/978-3-319-19773-9_',
                          'https://link.springer.com/chapter/10.1007/978-3-642-39112-5_',
                          'https://link.springer.com/chapter/10.1007/978-3-642-21869-9_']
    
    no_of_chapters = [50, 74, 45, 76, 45, 101, 83, 137, 165, 134]
    
    for i in range(0,len(chapter_url_prefix)):
        for j in range(1, no_of_chapters[i] + 1):
             paper_links.append(chapter_url_prefix[i] + str(j)+'\n')
    
    with open('conference-paper-links.txt', 'w') as file:
        file.writelines(paper_links)
        
def test_conference_paper_links():
    page = requests.get("https://link.springer.com/article/10.1007/s40593-013-0003-7")
    soup = BeautifulSoup(page.text, 'html.parser')
    with open("paper_requests_journal.html", "w", encoding="utf-8") as file:
        file.write(str(soup))