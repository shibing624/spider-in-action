# -*- coding: utf-8 -*-
"""
@description: 
@author:XuMing
"""
from __future__ import print_function  # 兼容python3的print写法
from __future__ import unicode_literals  # 兼容python3的编码处理

import os
import urllib
import urllib.request

from bs4 import BeautifulSoup


# import urllib2


# 抓取淘宝MM图
class TaoBaoMMSpider:
    def __init__(self):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}
        self.url = "https://mm.taobao.com/json/request_top_list.htm"

    def get_page(self, index):
        url = self.url + "?page=" + str(index)
        request = urllib.request.Request(url, headers=self.headers)
        resp = urllib.request.urlopen(request)
        return resp.read()

    # 获取索引界面所有MM的信息，list格式
    def get_content(self, index):
        page = self.get_page(index).decode('utf-8')
        contents = []
        soup = BeautifulSoup(page, 'lxml')
        items = soup.find_all('div', class_='list-item')
        for item in items:
            # item[0]个人详情URL,item[1]头像URL,item[2]姓名,item[3]年龄,item[4]居住地
            personal_info = item.find('div', class_='personal-info').find('a', class_='lady-name')
            personal_url = 'https:' + personal_info.get('href')
            name = personal_info.get_text()
            head_url = 'https:' + item.find('div', class_='personal-info').find('div', class_='pic-word') \
                .find('a', class_='lady-avatar').find('img').get('src')
            age = item.find('div', class_='personal-info').find('div', class_='pic-word').find('em') \
                .find('strong').get_text()
            address = item.find('div', class_='personal-info').find('div', class_='pic-word') \
                .find('p').find('span').string
            contents.append([personal_url, head_url, name, age, address])
        return contents

    # 获取MM个人详情页面
    def get_detail_page(self, info_url):
        # 构建请求的request
        request = urllib.request.Request(info_url, headers=self.headers)
        resp = urllib.request.urlopen(request)
        return resp.read().decode('gbk')

    # 获取个人相册地址
    def get_album_url(self, page):
        page = BeautifulSoup(page, 'lxml')
        menu = page.find('ul', class_='mm-p-men')
        if menu:
            return 'https:' + menu.find('a').get('href')
        return ""

    # 获取页面所有图片
    def get_all_img(self, page):
        page = BeautifulSoup(page, 'html.parser')
        img = page.find('div', class_='mm-p-model-info clearfix').find('img')
        if img:
            return 'https:' + img['src'].strip()
        return None

    # 保存多张写真图片
    def save_img(self, images, name):
        num = 1
        print(name, '共有', len(images), '张照片')
        if images is None:
            return
        for image_url in images:
            split_path = image_url.split('.')
            f_tail = split_path.pop()
            if len(f_tail) > 3:
                f_tail = 'jpg'
            file_name = name + '/' + str(num) + '.' + f_tail
            self.save_img(image_url, file_name)
            num += 1

    # 保存头像
    def save_icon(self, icon_url, name):
        split_path = icon_url.split('.')
        f_tail = split_path.pop()
        file_name = name + '/icon.' + f_tail
        self.save_img(icon_url, file_name)

    # 保存个人简介
    def save_brief(self, content, item):
        name = item[2]
        file_name = name + '/' + name + '.txt'
        f = open(file_name, "w+")
        print('在保存个人信息：', file_name)
        f.write(('名字：' + name + '\n').encode('utf-8'))
        f.write(('个人空间地址：' + item[0] + '\n').encode('utf-8'))
        f.write(('年龄：' + str(item[3]) + '\n').encode('utf-8'))
        f.write(('居住地：' + item[4] + '\n').encode('utf-8'))
        f.write(('个人相册地址：' + content + '\n').encode('utf-8'))
        f.close()

    # 传入图片地址，文件名，保存单张图片
    def save_img(self, image_url, file_name, index=0):
        if image_url is None:
            return
        try:
            urllib.urlretrieve(url=image_url, filename=file_name)
            print('下完了%s张' % (index + 1))
            index += 1
        except Exception:
            print('这张图片下载出问题了： %s' % image_url)

    # 创建新目录
    def mkdir(self, path):
        path = path.strip()
        if not os.path.exists(path):
            os.makedirs(path)

    def save_page_info(self, index):
        contents = self.get_content(index)
        for item in contents:
            # item[0]个人详情URL,item[1]头像URL,item[2]姓名,item[3]年龄,item[4]居住地
            print(u"名字:", item[2], u"芳龄", item[3], u",地址", item[4], u",个人页面", item[0])
            detail_url = item[0]
            detail_page = self.get_detail_page(detail_url)
            album_url = self.get_album_url(detail_page)
            images = self.get_all_img(detail_page)
            self.mkdir(item[2])
            self.save_brief(album_url, item)
            self.save_img(images, item[2])
            self.save_icon(item[1], item[2])

    def save_pages_info(self, start, end):
        for i in range(start, end + 1):
            self.save_page_info(i)


# 传入起止页码即可，在此传入了2,10,表示抓取第2到10页的MM
spider = TaoBaoMMSpider()
spider.save_pages_info(2, 3)
