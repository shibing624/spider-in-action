# -*- coding: utf-8 -*-
"""
@description: 爬糗事百科的段子
@author:XuMing
"""
from __future__ import print_function  # 兼容python3的print写法
from __future__ import unicode_literals  # 兼容python3的编码处理

import urllib2

from bs4 import BeautifulSoup


# 糗事百科爬虫类
class QSBKSpider:
    # 初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        # 存放程序是否继续运行的变量
        self.enable = False
        self.count = 0

    # 传入某一页的索引获得页面代码
    def get_page(self, page_index):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(page_index)
            # 构建请求的request
            request = urllib2.Request(url, headers=self.headers)
            # 利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            # 将页面转化为UTF-8编码
            page_code = response.read().decode('utf-8')
            return page_code

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print(u"连接糗事百科失败,错误原因", e.reason)
                return None

    # 传入某一页代码，返回本页不带图片的段子列表
    def get_page_items(self, page_index):
        page_code = self.get_page(page_index)
        soup = BeautifulSoup(page_code, "lxml")
        storys = soup.find_all("div", class_="article block untagged mb15")
        page_stories = []

        for story in storys:
            author = story.find("div", class_="author clearfix").find('h2').get_text()
            content = story.find("div", class_="content").find('span').get_text()
            self.count += 1
            page_stories.append((author, content, self.count))
        return page_stories

    # 加载并提取页面的内容，加入到列表中
    def load_page(self):
        # 如果当前未看的页数少于2页，则加载新一页
        if self.enable:
            if len(self.stories) < 2:
                # 获取新一页
                page_stories = self.get_page_items(self.pageIndex)
                # 将该页的段子存放到全局list中
                if page_stories:
                    self.stories.append(page_stories)
                    # 获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1

    # 调用该方法，每次敲回车打印输出一个段子
    def get_single_story(self, page_stories, page):
        # 遍历一页的段子
        for story in page_stories:
            # 等待用户输入
            input = raw_input()
            # 每当输入回车一次，判断一下是否要加载新页面
            self.load_page()
            # 如果输入Q则程序结束
            if input == "Q":
                self.enable = False
                return
            print(u"第%d页\t发布人:%s\t发布内容:%s\tID:%s" % (page, story[0], story[1], story[2]))

    # 开始方法
    def start(self):
        print(u"正在读取糗事百科,按回车查看新段子，Q退出")
        # 使变量为True，程序可以正常运行
        self.enable = True
        # 先加载一页内容
        self.load_page()
        # 局部变量，控制当前读到了第几页
        now_page = 0
        while self.enable:
            if len(self.stories) > 0:
                # 从全局list中获取一页的段子
                page_stories = self.stories[0]
                # 当前读到的页数加一
                now_page += 1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.get_single_story(page_stories, now_page)


spider = QSBKSpider()
spider.start()
