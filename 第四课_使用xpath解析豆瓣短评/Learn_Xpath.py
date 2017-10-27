#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree

url = 'https://book.douban.com/subject/1084336/comments/'
r = requests.get(url).text

s = etree.HTML(r)
print(s.xpath('//div[@class="comment"]/p/text()'))
