#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

r = requests.get('https://book.douban.com/subject/1084336/comments/').text

from bs4 import BeautifulSoup
soup = BeautifulSoup(r, 'lxml')
pattern = soup.find_all('p', 'comment-content')
for item in pattern:
    print(item.string)

import pandas

comments = []
for item in pattern:
    comments.append(item.string)
df = pandas.DataFrame(comments)
df.to_csv('comments.csv')
