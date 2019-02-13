#!/usr/bin/env python
# coding=utf-8
# 获得各城市的区县相关信息

import requests
from lxml import etree
from .city import cities
from ..core.xpath import CITY_DISTRICT_XPATH
from ..request.headers import create_headers
from ..config import SPIDER_NAME

chinese_city_district_dict = dict()     # 城市代码和中文名映射



def get_chinese_district(en):
    """
    拼音区县名转中文区县名
    :param en: 英文
    :return: 中文
    """
    return chinese_city_district_dict.get(en, None)


def get_districts(city):
    """
    获取各城市的区县中英文对照信息
    :param city: 城市
    :return: 英文区县名列表
    """
    url = 'https://{0}.{1}.com/xiaoqu/'.format(city, SPIDER_NAME)
    headers = create_headers()
    response = requests.get(url, timeout=10, headers=headers)
    html = response.content
    root = etree.HTML(html)
    elements = root.xpath(CITY_DISTRICT_XPATH)
    en_names = list()
    ch_names = list()
    for element in elements:
        link = element.attrib['href']
        en_names.append(link.split('/')[-2])
        ch_names.append(element.text)

        # 打印区县英文和中文名列表
    for index, name in enumerate(en_names):
        chinese_city_district_dict[name] = ch_names[index]
        # print(name + ' -> ' + ch_names[index])
    return en_names


if __name__ == '__main__':
    for key in cities.keys():
        # 寻找那些网页格式不合规的城市
        chinese_city_district_dict = dict()
        get_districts(key)
        if len(chinese_city_district_dict.items()) == 0:
            print(key)
