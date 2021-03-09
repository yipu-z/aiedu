# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# request main page
page_main = requests.get("https://www.tandfonline.com/toc/hlns20/current")

soup_main = BeautifulSoup(page_main.text, 'html.parser')

links_main =  [a['href'] for a in soup_main.find_all('a', href=True)]

links_main = [l for l in links_main if '/action/tocQuickLink?quickLinkJournal=hlns20&quickLinkId=vhlns' in l]


# Get each article page links

article = []

for link_issue in links_main:
    page_issue = requests.get("https://www.tandfonline.com" + link_issue)
    soup_issue = BeautifulSoup(page_issue.text, 'html.parser')
    link_article = [a['href'] for a in soup_issue.find_all('a', href=True)]
    link_article = [l for l in link_article if '/doi/' in l]
    link_article = list(set(link_article))
    article.extend(link_article)

# get doi from article pages
doi = [l.replace("/doi/suppl/", "")
       .replace("/doi/full/", "")
       .replace("/doi/abs/", "")
       .replace("/doi/ref/", "")
       .replace("/doi/pdf/", "") for l in article]

doi = list(set(doi))

doi_list = []
for eachdoi in doi:
    subdoi = eachdoi.split("/")
    doi_list.append(subdoi)

# get formatted doi links
# e.g. https://www.tandfonline.com/action/showCitFormats?doi=10.1080%2F10508406.1998.9672060
citlink_list = []
for eachdoi in doi_list:
    citlink = "https://www.tandfonline.com/action/showCitFormats?doi=" + eachdoi[0] + "%2F" + eachdoi[1]
    citlink_list.append(citlink)

# Save citation links
with open("jls.txt", "w", encoding="utf-8") as file:
    file.write(str(citlink_list))

"""
# TODO

# Selenium 
# Set user data dir
options = webdriver.ChromeOptions()
# Type in user own data dir
options.add_argument("user-data-dir=C:\\Users\\Jane\\AppData\\Local\\Google\\Chrome\\User Data")
# Set driver
driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options=options)

driver.get(citlink_list[0])
"""