# -*- coding:utf-8 -*-
#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.baidu.com")

elem = driver.find_element_by_xpath('//*[@id="kw"]')
elem.send_keys("Python selenium", Keys.ENTER)
print(driver.page_source)

