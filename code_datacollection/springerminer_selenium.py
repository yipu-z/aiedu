# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 02:16:39 2020

@author: Jie Chen

--app-id=dfcockecdchbdphebindblhbjhjmgifo
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re

domain_url = "https://link.springer.com"
book_url = "/book/10.1007/978-3-030-52237-7"
paper_url = "/article/10.1007/s40593-020-00210-6"

# Set user data dir
options = webdriver.ChromeOptions()
# Type in user own data dir
options.add_argument("user-data-dir=C:\\Users\\Jane\\AppData\\Local\\Google\\Chrome\\User Data")
# Set driver
driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=options)

def get_book_html(url):
    # Open url in the driver
    driver.get(url)
    html = driver.page_source
    
    rule = r'\/([^\/]*)$'
    filename = re.findall(rule, url)[0]
    
    with open(filename + ".html", "w", encoding="utf-8") as file:
        file.write(html)
    
    paper_links = []
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all(class_="content-type-list__link u-interface-link")
    for link in links:
        paper_links.append(domain_url + link['href'])
        
    no_of_chapters = soup.find(class_="c-tabs__deemphasize").text
    no_of_chapters = re.findall(r'\d+', no_of_chapters)[0]
    no_of_chapters = int(no_of_chapters)
    
    page_number = soup.find(id="page-number")['value']
    page_number = int(page_number)
    
    max_page_number = soup.find(class_="test-maxpagenum").text
    max_page_number = int(max_page_number)
    
    try:
        if page_number < max_page_number:
            page_number += 1
            book_url_next = book_url + "?page=" + str(page_number)
            print(get_book_html(domain_url + book_url_next))
            paper_links.append(get_book_html(book_url_next))
    except:
        pass
    
    return paper_links

def get_paper_html(url):
    driver.get(url)
    html = driver.page_source
    with open("paper.html", "w", encoding="utf-8") as file:
        file.write(html)


paper_links = get_book_html(domain_url + book_url)

