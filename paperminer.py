# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 05:01:41 2020

@author: Jie Chen
"""

# IAIED Abstract Miner
import os
import re
import sys
import requests
from bs4 import BeautifulSoup
import json

def get_abstract_iaied(url, saveoption):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        text = soup.find('script', type='text/javascript').text
        rule = r'window.__NUXT__=(.*?);$'
        text = re.findall(rule, text)[0]
        data = json.loads(text)
        abstract = data['state']['currentPublication']['fields']['abstract']
    except:
        print('Error occurred. Please make sure the url exists: ' + url)
    else:
        return abstract
    return None
 
def save_abstract_iaied(serial, abstract):
    filepath = './iaied/' + serial + '.txt'
    if os.path.exists(filepath):
        print(filepath + ' already exists. Will not override.')
    else: 
        txt = open(filepath, 'w')
        try:    
           txt.write(abstract)
        except:
            txt.close()
            print('[Error] IAIED Serial ' + serial + ' not saved.')
            os.remove(filepath)
            return False
        else:
            print('[Success] IAIED Serial ' + serial + ' saved as ' + filepath)
            txt.close()
            return True
    return False

choice = input('IAIED Data Miner. \nThe format of IAIED papers is \'https://iaied.org/journal/\' + serial number. \nPlease select choice: \n1 Extract single journal\n2 Extract multiple journals \nYour choice: ')
saveoption = input('Save abstract text under iaied folder? (y/n) \nYour answer (y for yes, n for no): ')

if 'y' == saveoption:
    folderpath = './iaied'
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)

if choice == '1':
    serial = input('Please enter serial number: ')
    url = 'https://iaied.org/journal/' + serial
    print('Mining abstract on https://iaied.org/journal/' + serial)
    abstract = get_abstract_iaied(url, saveoption)
    if 'y' == saveoption and abstract is not None:
        save_abstract_iaied(serial, abstract)
    
elif choice == '2':
    first = input('Please enter the minimum serial number: ')
    last = input('Please enter the maximum serial number: ')
    print('Mining abstract on https://iaied.org/journal/' + first + '~' + last)
    for serial in range(int(first), int(last)+1):
        url = 'https://iaied.org/journal/' + str(serial)
        abstract = get_abstract_iaied(url, saveoption)
        if 'y' == saveoption:
            save_abstract_iaied(str(serial), abstract)


