#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import pandas as pd
import time

headers = {
    'authorization':'Bearer Mi4xUUhNc0FnQUFBQUFBa0FLVnVud3hEQmNBQUFCaEFsVk5oeW5qV1FBcmVhY2F0VUhWenJTc1hVcUlycW1tRzAtMXpB|'\
    '1505467527|b43e672333e0fe298111f2b18ed9e52c9f8f23d7',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3192.0 Safari/537.36',
}

user_data = []

def get_user_data(page):
    for i in range(page):
        url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}&limit=20'.format(i*20)
        response = requests.get(url, headers=headers).json()
        user_data.extend(response['data'])
        print("成功爬取第%s页" % str(i+1))
        time.sleep(1)

if __name__ == '__main__':
    get_user_data(117)
    df = pd.DataFrame.from_dict(user_data)
    df.to_csv('user.csv')
