#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 20:13:34 2019

@author: manzar
"""
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

url = "https://www.adepta.com/en/our-members/"

wb = webdriver.Chrome()
wb.get(url)

for i in range(100):
    try:
        wb.find_element_by_class_name('adp_charger_plus').click()
        time.sleep(2)
    except:
        break

html = wb.execute_script('return document.documentElement.outerHTML')
soup = BeautifulSoup(html, 'lxml')

links = []
refs = soup.findAll('h3')
for ref in refs:
    try:
        links.append(ref.a.attrs['href'])
        print(ref.a.attrs['href'])
    except:
        pass
    
wb.close()

header = 'Company Name, Email, Telephone, Website\n'
file = open('assignment.csv', 'w')
file.write(header)

for link in links:
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    name = soup.findAll('h2')[0].text
    tel = soup.findAll('div', {'class': 'telephone'})[0].a.attrs['href'].split('tel:')[1]
    web = soup.findAll('div', {'class': 'bouton-site-internet'})[0].a.attrs['href']
    email = soup.findAll('div', {'class': 'bouton-contact'})[0].a.attrs['href'].split('mailto:')[1]
    print(name, email, web, tel)
    file.write(name.replace(',', '') + ', ' + email + ', ' + tel + ', ' + web + '\n')
file.close()