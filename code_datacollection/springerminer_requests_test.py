# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 09:59:37 2020

@author: Jie Chen
"""
import re
import time
import requests
from bs4 import BeautifulSoup

# Open conference-paper-links.txt to get links
with open('conference-paper-links.txt') as file:
    # Store links into an array called lines
    lines = file.readlines()
    # Loop lines
    for line in lines:
        # Send Internet request to each link
        page = requests.get(line)
        # Parse the html from the link
        soup = BeautifulSoup(page.text, 'html.parser')
        # Use regular expression to generate file name
        rule = r'\/([^\/]*)$'
        filename = re.findall(rule, line)[0]
        # Save the html into file
        with open(filename + ".html", "w", encoding="utf-8") as file:
            file.write(str(soup))

"""
time.sleep(2)

    headers = {'Content-Type': "application/json;charset=uf8"}
    url = baseurl + path
    response = None
    try:
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()

        s.keep_alive = False
        response = requests.post(url, data=data, headers=headers,stream=False,timeout= 10)

        response.close()
        del(response)  
    except Exception as indentfier:

        time.sleep(5)
        timer = threading.Timer(timerFlag, upload_position)
        timer.start()
"""