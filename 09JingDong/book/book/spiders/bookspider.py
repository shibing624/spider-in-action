# -*- coding: utf-8 -*-
"""
@description: 
@author:XuMing
"""
from __future__ import print_function  # 兼容python3的print写法
from __future__ import unicode_literals  # 兼容python3的编码处理

import json
import re

import requests
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider

from book.items import BookItem


class BookSpider(CrawlSpider):
    name = 'BookSpider'
    start_urls = ['http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10001-1#comfort']

    def parse(self, response):
        item = BookItem()
        selector = Selector(response)
        books = selector.xpath('/html/body/div[8]/div[2]/div[3]/div/ul/li')
        for each in books:
            num = each.xpath('div[@class="p-num"]/text()').extract()
            book_name = each.xpath('div[@class="p-detail"]/a/text()').extract()
            # body > div.w.clearfix > div.g-main > div.m.m-list > div > ul > li.fore1 > div.p-detail > dl:nth-child(2) > dd > a
            # /html/body/div[8]/div[2]/div[3]/div/ul/li[1]/div[3]/dl[1]/dd/a
            author = each.xpath('div[@class="p-detail"]/dl[1]/dd/a[1]/text()').extract()
            # html/body/div[8]/div[2]/div[3]/div/ul/li[1]/div[3]/dl[2]/dd/a
            press = each.xpath('div[@class="p-detail"]/dl[2]/dd/a/text()').extract()
            temphref = each.xpath('div[@class="p-detail"]/a/@href').extract()
            temphref = str(temphref)

            book_id = str(re.search('com/(.*?)\.html', temphref).group(1))
            json_url = 'http://p.3.cn/prices/mgets?skuIds=J_' + book_id
            r = requests.get(json_url).text
            data = json.loads(r)[0]
            price = data['m']
            discount_price = data['p']

            item['number'] = num
            item['bookID'] = book_id
            item['bookName'] = book_name
            item['author'] = author
            item['price'] = price
            item['discountPrice'] = discount_price
            item['press'] = press

            yield item

        next_link = selector.xpath('/html/body/div[8]/div[2]/div[4]/div/div/span/a[7]/@href').extract()
        if next_link:
            next_link = next_link[0]
            print('next_link:',next_link)
            yield Request(url='http:' + next_link, callback=self.parse)
