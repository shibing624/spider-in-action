#!/usr/bin/env python
# coding=utf-8
# 用于获取代理

from bs4 import BeautifulSoup
import requests
from .headers import create_headers
from ..config import proxy_url
proxys_src = []
proxys = []


def spider_proxyip(num=10):
    try:
        req = requests.get(proxy_url, headers=create_headers())
        source_code = req.content
        print(source_code)
        soup = BeautifulSoup(source_code, 'lxml')
        ips = soup.findAll('tr')

        for x in range(1, len(ips)):
            ip = ips[x]
            tds = ip.findAll("td")
            proxy_host = "{0}://".format(tds[5].contents[0]) + tds[1].contents[0] + ":" + tds[2].contents[0]
            proxy_temp = {tds[5].contents[0]: proxy_host}
            proxys_src.append(proxy_temp)
            if x >= num:
                break
    except Exception as e:
        print("spider_proxyip exception:")
        print(e)


if __name__ == '__main__':
    spider_proxyip(10)
    print(proxys_src)
