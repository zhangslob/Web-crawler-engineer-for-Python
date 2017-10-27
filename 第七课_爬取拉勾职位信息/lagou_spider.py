# -*- coding:utf-8 -*-
#!/usr/bin/env python

import requests
from pymongo import MongoClient
import time
from fake_useragent import UserAgent

client = MongoClient()
db=client.test
lagou = db.lagou

headers = {
    'Cookie': 'user_trace_token=20170829113503-601dde19-9bd8-49cc-b849-0b2a33350010; LGUID=20170829113504-0bb3cbe9-8c6b-11e7-8faa-5254005c3644; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=ABAAABAABEEAAJA39A764F44E13E57EFF2EDDF05DE9CC31; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_search; SEARCH_ID=b4638bec573e472295c1c80f625fb3a6; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1506505446,1506506472,1506755951,1507606209; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1507606215; _ga=GA1.2.1581214308.1503977706; LGSID=20171010113009-513cd20c-ad6b-11e7-8519-525400f775ce; LGRID=20171010113015-54adf399-ad6b-11e7-9455-5254005c3644',  
    'Referer': 'https://www.lagou.com/jobs/list_python?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=',
}


def get_job_info(page, kd):
    for i in range(page):
        url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false&isSchoolJob=0'
        payload = {
            'first':'false',
            'pn':str(i),
            'kd': kd,
        }

        ua = UserAgent()
        headers['User-Agent'] = ua.random
        response = requests.post(url, data=payload, headers=headers)

        if response.status_code == 200:
            job_json = response.json()['content']['positionResult']['result']
            lagou.insert(job_json)
            #print(job_json)       

        else:
            print('Something Wrong!' )

        print('正在爬取第 ' + str(i) + ' 页的数据...')
        time.sleep(3)

if __name__ == '__main__':
    get_job_info(31, 'Python')
    
