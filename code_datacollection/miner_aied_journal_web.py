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
import os

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
    
    for url in link:
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

def get_html_year():
    path_in = "../data/JAIED_19892020_web/iaied_journal_html_8920_sum/"
    d = {}
    for file_in in os.listdir(path_in):
        with open(path_in + file_in, "r", encoding = 'utf') as infile:
            year = file_in.strip(".html").strip('/journal/')
            html_text = infile.read()
            soup = BeautifulSoup(html_text, 'html.parser')
            link_of_text = [link.get('href') for link in soup.find_all('a')]
            link_of_text = [l for l in link_of_text if l is not None and '/journal/' in l and 'springer' not in l and 'redirect' not in l]
            link_of_text = list(set(link_of_text))
            link_of_text = [l.strip('/journal/') + '.html' for l in link_of_text]
            d[year] = link_of_text
    return d

def get_journal_paper_html_json_new():
    path_in = "../data/JAIED_19892020_web/iaied_journal_html_8920/"
    
    d = get_html_year()
    
    for file_in in os.listdir(path_in):
        
        for key,value in d.items():
            if file_in in value:
                publication_year = key
                
        with open(path_in + file_in, "r", encoding = 'utf') as infile:
            text = infile.read()
            soup = BeautifulSoup(text, 'html.parser')
            
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
                if author:
                    author_split = []
                    for auth in author:
                        author_name = ''
                        affiliation = ''
                        if ',' in auth:
                            author_array = auth.split(',', maxsplit=1)
                            author_name = author_array[0].strip()
                            affiliation = author_array[1].strip()
                        else:
                            author_name = auth.strip()
                            affiliation = ''
                        author_split.append({'author-name' : author_name, 'affiliation' : affiliation})
                
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
                    'author' : author_split,
                    'page-info' : pages_text,
                    'publication-year' : publication_year,
                    'keywords' : keywords_list,
                    'abstract' : abstract_text
                    }
                
                filename = file_in.replace('html', 'json')
                jsonfolder_out = "../data/JAIED_19892020_web/iaied_journal_json_8920_/"
                with open(jsonfolder_out + filename, "w", encoding="utf-8") as file:
                    json.dump(data, file)
                    
def get_conference_fullpaper_text():
    
    path_in = "../data/AIED_20112020/iaied_conf_html_1120/"
    path_out = "../data/AIED_20112020/iaied_conf_text_1120/"
    
    result = []
    for file_in in os.listdir(path_in):
        with open(path_in + file_in, "r", encoding = 'utf') as infile:
            name = file_in
            text = infile.read()
            soup = BeautifulSoup(text, 'html.parser')
            if soup.find(id = "body"):
                full = soup.find(id = "body").text
                filename_out = name.replace('html', 'txt')
                filepath_out = path_out + filename_out
                with open(filepath_out, "w", encoding='utf-8') as outfile:
                     outfile.write(full)

def get_springer_journal_paper_html():
    link = []
    with open("journal-paper-links.txt", "r") as file:
        for line in file:
            link.append(line.strip())
    
    for url in link:
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
                
            htmlfolder_out = "../data/JAIED_20132020/iaied_journal_html_1320/"
            rule = r'\/([^\/]*)$'
            filename = re.findall(rule, url)[0]
            with open(htmlfolder_out + filename + ".html", "w", encoding="utf-8") as file:
                file.write(str(soup))
        except Exception as e:
            print(e)

def get_journal_fullpaper_text():
    
    path_in = "../data/JAIED_20132020/iaied_journal_html_1320/"
    path_out = "../data/JAIED_20132020/iaied_journal_text_1320/"
    
    result = []
    for file_in in os.listdir(path_in):
        with open(path_in + file_in, "r", encoding = 'utf') as infile:
            name = file_in
            text = infile.read()
            soup = BeautifulSoup(text, 'html.parser')
            if soup.find(class_="c-article-body"):
                text = ""
                if soup.find(attrs={"aria-labelledby":"Sec1"}):
                    sib = soup.find(attrs={"aria-labelledby":"Sec1"})           
                    while sib['aria-labelledby'] != 'Bib1':
                        print(sib['aria-labelledby'])
                        text += sib.text + "\n"
                        sib = sib.next_sibling
                        if sib == '\n':
                             break
                if text:
                    filename_out = name.replace('html', 'txt')
                    filepath_out = path_out + filename_out
                    with open(filepath_out, "w", encoding='utf-8') as outfile:
                         outfile.write(text)
