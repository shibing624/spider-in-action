# -*- coding: utf-8 -*-
"""
@description: 百度贴吧
@author:XuMing
"""
from __future__ import print_function  # 兼容python3的print写法
from __future__ import unicode_literals  # 兼容python3的编码处理

import urllib2

from bs4 import BeautifulSoup


# 百度贴吧爬虫类
class BaiduTieBaSpider:
    def __init__(self, base_url, see_lz, floor_tag):
        self.base_url = base_url
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}
        # 是否只看楼主
        self.see_lz = '?see_lz=' + str(see_lz)
        # 全局file变量，文件写入操作对象
        self.file = None
        # 楼层标号，初始为1
        self.floor = 1
        # 默认的标题
        self.default_title = u"百度贴吧"
        self.count = 0
        # 是否写入楼分隔符的标记
        self.floor_tag = floor_tag

    # 传入页码，获取页面内容
    def get_page(self, page_num):
        try:
            url = self.base_url + self.see_lz + '&pn=' + str(page_num)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            page = response.read().decode('UTF-8')
            if len(page) == 0:
                print(u"获取百度贴吧页面源文件失败")
                exit(1)
            return page
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print(u"连接百度贴吧失败,错误原因", e.reason)
                return None

    def get_title(self):
        page = self.get_page(1)
        soup = BeautifulSoup(page, 'lxml')
        title = soup.find('div', class_='pb_content clearfix')\
            .find('div',class_='core_title_wrap_bright clearfix')\
            .find('h3').get_text()
        return title

    def get_page_num(self):
        page = self.get_page(1)
        soup = BeautifulSoup(page, 'lxml')
        num = soup.find('li', class_='l_reply_num').find('span').get_text()
        if num:
            return num
        else:
            return None

    def get_content(self, page):
        content = []
        soup = BeautifulSoup(page, 'lxml')
        pb_content = soup.find_all('div', class_='pb_content clearfix')
        for segment_content in pb_content:
            text = segment_content.find_all('div', class_='d_post_content j_d_post_content ')\
                .get_text()
            content.append(text)
        return content

    def set_file_title(self, title):
        if title is not None:
            self.file = open(title + ".txt", "w+")
        else:
            self.file = open(self.default_title + ".txt", "w+")

    def write_data(self, contents):
        for item in contents:
            if self.floor_tag == '1':
                floor_line = "\n" + str(self.floor) + u"-----------\n"
                self.file.write(floor_line)
            self.file.write(item)
            self.floor += 1

    def start(self):
        index_page = self.get_page(1)
        page_num = self.get_page_num(index_page)
        title = self.get_title(index_page)
        self.set_file_title(title=title)
        if page_num is None:
            print("URL 已失效，请重试")
            return
        try:
            print("该帖子共有" + str(page_num) + "页")
            for i in range(1, int(page_num) + 1):
                page = self.get_page(i)
                contents = self.get_content(page)
                self.write_data(contents)
                print("已经写入第" + str(i) + "页数据")
        except IOError, e:
            print("写入异常，原因：" + e.message)
        finally:
            print("写入任务完成")


# print(u"请输入帖子代号")
base_url = 'https://tieba.baidu.com/p/' + '5033072119'#str(raw_input(u''))
see_lz =1 #raw_input("是否只获取楼主发言，是输入1，否输入0\n")
floor_tag =1 # raw_input("是否写入楼层信息，是输入1，否输入0\n")
spider = BaiduTieBaSpider(base_url, see_lz, floor_tag)
spider.start()
