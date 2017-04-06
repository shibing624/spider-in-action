# -*- coding: utf-8 -*-
"""
@description: 通过关键词（行业名、城市名）搜索职位
@author:XuMing
"""
from __future__ import print_function  # 兼容python3的print写法
from __future__ import unicode_literals  # 兼容python3的编码处理

import json
import urllib2
from multiprocessing.dummy import Pool as ThreadPool
from urllib import urlencode
from urlparse import urlparse, parse_qs  # py2
import time
import pandas as pd
from pandas import DataFrame, Series


class JobSpider():
    # 初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化headers
        # self.headers = {'User-Agent': self.user_agent}
        self.headers = {
            "X-Requested-With": 'XMLHttpRequest',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Origin": 'https://www.lagou.com',
            "Cookie": 'user_trace_token=20170211115515-2db01e4efbb24178989f2b6139d3698e; LGUID=20170211115515-e593a6c4-f00d-11e6-8f71-5254005c3644; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E5%85%A8%E5%9B%BD; login=false; unick=""; _putrc=""; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486785316; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486789519; _ga=GA1.2.1374329991.1486785316; LGRID=20170211130519-af0ec03c-f017-11e6-a32c-525400f775ce; TG-TRACK-CODE=search_code; JSESSIONID=A5AC6E7C54130E13C1519ABA7F70BC3C; SEARCH_ID=053c985ab53e463eb5f747658872ef29',
            "Connection": 'keep-alive'
        }

    def search_page_count(self, position, city):
        try:
            url = 'http://www.lagou.com/jobs/positionAjax.json?'
            params = {'city': city, 'kd': position}
            url += urlencode(params)
            proxy = urllib2.ProxyHandler({'http': '180.213.110.43:8080'})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            response = urllib2.urlopen(url)
            time.sleep(1)

            print(response.read())

            # # 构建请求的request
            # request = urllib2.Request(url, headers=self.headers)
            # # 利用urlopen获取页面代码
            # response = urllib2.urlopen(request)

            # 将页面转化为UTF-8编码
            data = response.read().decode('utf8')
            if data is None:
                raise Exception
            content = json.loads(data, encoding='utf-8')['content']
            count = int(content['positionResult']['resultSize'])
            # count = int(content['positionResult']['totalCount'])
            print('搜索到 {0} 个职位'.format(count))
            return count
        except Exception, e:
            print(u"连接拉勾网失败,错误原因", e)
            return None

    def get_rdata(self, url):
        # 构建请求的request
        request = urllib2.Request(url, headers=self.headers)
        # 利用urlopen获取页面代码
        response = urllib2.urlopen(request)
        # 将页面转化为UTF-8编码
        data = response.read().decode('utf8')
        params = parse_qs(urlparse(url).query)
        print('正在解析第{0}页'.format(params.get('pn', [''])[0]))

        # json
        json_data = json.loads(data, encoding='utf-8')['content']['positionResult']['result']
        try:
            for i in list(range(len(json_data))):
                label_list = json_data[i]['companyLabelList']
                if isinstance(label_list, list):
                    json_data[i]['companyLabelListTotal'] = '-'.join(json_data[i]['companyLabelList'])
                    json_data[i].pop('companyLabelList')

                    if i == 0:
                        rdata = DataFrame(Series(data=json_data[i])).T
                    else:
                        rdata = pd.concat([rdata, DataFrame(Series(data=json_data[i])).T])
            return rdata
        except Exception, e:
            print(e.message)
            return None

    def search_jobs_by_keyword(self, position, city):
        # total page count
        page_count = self.search_page_count(position, city)
        if page_count is None:
            print(u"连接拉勾网失败",)
            return
        if page_count == 0:
            print('抱歉！在您搜索的城市中没有您要找的职位')
            return
        total_data = DataFrame().T
        urls = []
        for i in range(0, page_count):
            url = 'http://www.lagou.com/jobs/positionAjax.json?'
            params = {'city': city, 'kd': position, 'pn': i + 1}
            url += urlencode(params)
            urls.append(url)
        # work num
        pool = ThreadPool(processes=1)
        rdatas = pool.map(self.get_rdata, urls)
        for rdata in rdatas:
            total_data = pd.concat([total_data, rdata])
        total_data.to_csv('lagou_jobs.csv')


# position = input('请输入你要爬取的职位:')
# city = input('请输入你要爬取的城市:')
# search_jobs_by_keyword(position, city)
job = JobSpider()
job.search_jobs_by_keyword('NLP', '')
