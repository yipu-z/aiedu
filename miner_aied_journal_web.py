# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 09:57:43 2020

@author: Jie Chen
"""

from selenium import webdriver
import time 
from bs4 import BeautifulSoup
import requests
import re
import json

def get_webpage_by_year():
    
    driver = webdriver.Chrome()
    
    driver.get("https://iaied.org/journal/")
    
    time.sleep(10)
    
    elem = driver.find_elements_by_css_selector("#__layout > div > div > section.section.journal_results > div > div > div.column.is-3.journalfilters > div > aside > ul > li > a")
    
    page = []
    
    count = 0
    for e in elem:
        e.click()
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        with open(str(count) + ".html", "w", encoding="utf-8") as file:
            file.write(str(soup))
        count += 1

def get_journal_paper_links():
    
    path = "../data/JAIED_19892020_web/iaied_journal_html_8920_sum/"
    
    link = []
    
    num = 31
    
    for i in range(0, 31):
        filepath = path + str(i) + ".html"
        with open(filepath, 'rb') as file:
            html_text = file.read()
        soup = BeautifulSoup(html_text, 'html.parser')
        link_of_text = [link.get('href') for link in soup.find_all('a')]
        link_of_text = [l for l in link_of_text if l is not None and '/journal/' in l and 'springer' not in l and 'redirect' not in l]
        link.extend(link_of_text)
        
    link = list(set(link))

    with open('journal-paper-web-links.txt', 'w') as file:
        for l in link:
            file.writelines('https://iaied.org' + l)

def get_journal_paper_html_json():
    link = []
    with open("journal-paper-web-links.txt", "r") as file:
        for line in file:
            link.append(line.strip())
    
    for url in link[100:]:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
    
        if soup.h3:
            article_title = soup.h3.text
            
            content = soup.find(class_='content')
            
            author = []
            if content.find("p",text=re.compile(r'Authors')):
                auth_title = content.find("p",text=re.compile(r'Authors'))
                auth_ul = auth_title.next_sibling
                auth_li = auth_ul.find_all('li')
                for li in auth_li:
                    author.append(li.text)
            
            pages_text = ""
            if content.find("p",text=re.compile(r'Pages')):
                pages_title = content.find("p",text=re.compile(r'Pages'))
                pages_text = pages_title.next_sibling.text
            
            keywords_list = ""
            if content.find("p",text=re.compile(r'Keywords')):
                keywords_title = content.find("p",text=re.compile(r'Keywords'))
                keywords_text = keywords_title.next_sibling.text
                keywords_list = keywords_text.split(',')
                keywords_list = [k.strip() for k in keywords_list]
            
            abstract_text = ""
            if content.find("p",text=re.compile(r'Abstract')):
                abstract_title = content.find("p",text=re.compile(r'Abstract'))
                abstract_text = abstract_title.next_sibling.text
            
            data = {
                'article-title': article_title,
                'author' : author,
                'page-info' : pages_text,
                'keywords' : keywords_list,
                'abstract' : abstract_text
                }
            
            htmlfolder_out = "../data/JAIED_19892020_web/iaied_journal_html_8920/"
            rule = r'\/([^\/]*)$'
            filename = re.findall(rule, url)[0]
            with open(htmlfolder_out + filename + ".html", "w", encoding="utf-8") as file:
                file.write(str(soup))
                
            jsonfolder_out = "../data/JAIED_19892020_web/iaied_journal_json_8920/"
            with open(jsonfolder_out + filename + ".json", "w", encoding="utf-8") as file:
                json.dump(data, file)