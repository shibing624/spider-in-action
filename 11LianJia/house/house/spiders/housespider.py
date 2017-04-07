# -*- coding: utf-8 -*-
"""
@description: 链家二手房信息
@author:XuMing
"""
from __future__ import print_function  # 兼容python3的print写法
from __future__ import unicode_literals  # 兼容python3的编码处理

import re
import time

import requests
import scrapy
from lxml import etree
from scrapy_redis.spiders import RedisSpider

from ..items import HouseItem


class HouseSpider(RedisSpider):
    name = 'house'
    redis_key = 'lianjia_house:urls'
    start_urls = [

        'http://wh.lianjia.com/ershoufang/',
        'http://sz.lianjia.com/ershoufang/',
        'http://bj.lianjia.com/ershoufang/',
    ]


    # 初始化方法，定义一些变量
    def __init__(self,policy=None, check_expired_frequency=100):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}

    def start_requests(self):
        if isinstance(self.start_urls, list):
            for url in self.start_urls:
                # deal with redirect
                yield scrapy.Request(url=url, headers=self.headers, meta={
                    'dont_redirect': True,
                    'cookiejar': 1
                }, method='GET',  callback=self.parse)

    def parse(self, response):
        lists = response.body.decode('utf-8')
        selector = etree.HTML(lists)
        # /html/body/div[3]/div[1]/dl[2]/dd/div[1]/div/a[1]
        # /html/body/div[3]/div[1]/dl[2]/dd/div[1]/div/a[15]
        # /html/body/div[3]/div[1]/dl[2]/dd/div[1]/div/a[1]
        # /html/body/div[3]/div[1]/dl[2]/dd/div[1]/div/a[1]
        area_list = selector.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div[1]/div/a')
        for area in area_list:
            try:
                area_han = area.xpath('text()').pop()  # 地点
                area_pin = area.xpath('@href').pop().split('/')[2]  # 拼音
                area_url = 'http://bj.lianjia.com/ershoufang/{}/'.format(area_pin)
                print(area_url)
                yield scrapy.Request(url=area_url, headers=self.headers, callback=self.detail_url,
                                     meta={"id1": area_han, "id2": area_pin})
            except Exception as e:
                print('error', e.message)
                pass

    def get_latitude(self, url):  # 进入每个房源链接抓经纬度
        p = requests.get(url)
        contents = etree.HTML(p.content.decode('utf-8'))
        latitude = contents.xpath('/ html / body / script[19]/text()').pop()
        time.sleep(3)
        regex = '''resblockPosition(.+)'''
        items = re.search(regex, latitude)
        content = items.group()[:-1]  # 经纬度
        longitude_latitude = content.split(':')[1]
        return longitude_latitude[1:-1]

    def detail_url(self, response):
        # 'http://bj.lianjia.com/ershoufang/dongcheng/pg2/'
        for i in range(1, 10):
            url = 'http://bj.lianjia.com/ershoufang/{}/pg{}/'.format(response.meta["id2"], str(1))
            time.sleep(2)
            try:
                contents = requests.get(url)
                contents = etree.HTML(contents.content.decode('utf-8'))
                houses = contents.xpath('/html/body/div[4]/div[1]/ul/li')
                for house in houses:
                    try:
                        item = HouseItem()
                        item['title'] = house.xpath('div[1]/div[1]/a/text()').pop()
                        item['community'] = house.xpath('div[1]/div[2]/div/a/text()').pop()
                        item['model'] = house.xpath('div[1]/div[2]/div/text()').pop().split('|')[1]
                        item['area'] = house.xpath('div[1]/div[2]/div/text()').pop().split('|')[2]
                        item['focus_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[0]
                        item['watch_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[1]
                        item['time'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[2]
                        item['price'] = house.xpath('div[1]/div[6]/div[1]/span/text()').pop()
                        item['average_price'] = house.xpath('div[1]/div[6]/div[2]/span/text()').pop()
                        item['link'] = house.xpath('div[1]/div[1]/a/@href').pop()
                        item['city'] = response.meta["id1"]
                        self.url_detail = house.xpath('div[1]/div[1]/a/@href').pop()
                        item['Latitude'] = self.get_latitude(self.url_detail)
                    except Exception:
                        pass
                    yield item
            except Exception:
                pass
