#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree

url = 'https://book.douban.com/subject/1084336/comments/'
r = requests.get(url).text

s = etree.HTML(r)
file = s.xpath('//div[@class="comment"]/p/text()')

import pandas as pd
df = pd.DataFrame(file)
df.to_excel('pinglun.xlsx')


#使用open保存

''' 
with open('pinglun.txt', 'w', encoding='utf-8') as f:
	for i in file:
		f.write(i)
'''

