# -*- coding: utf-8 -*-
# Author: LiangJun, XuMing <xuming624@qq.com>
# Brief: 

import re
from urllib import parse

import requests
from bs4 import BeautifulSoup
from multiprocessing import Lock, Pool
import time


class crawler:
    '''爬百度搜索结果的爬虫'''
    url = u''
    urls = []
    o_urls = []
    html = ''
    total_pages = 2
    current_page = 0
    next_page_url = ''
    timeout = 60  # 默认超时时间为60秒
    headersParameters = {  # 发送HTTP请求时的HEAD信息，用于伪装为浏览器
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}

    def __init__(self, keyword="尼康"):
        self.url = u'https://www.baidu.com/baidu?wd=' + parse.quote_plus(keyword) + '&tn=monline_dg&ie=utf-8'
        print(self.url)

    def set_timeout(self, time=timeout):
        '''设置超时时间，单位：秒'''
        try:
            self.timeout = int(time)
        except:
            pass

    def set_total_pages(self, num=total_pages):
        '''设置总共要爬取的页数'''
        try:
            self.total_pages = int(num)
        except:
            pass

    def set_current_url(self, url):
        '''设置当前url'''
        self.url = url

    def switch_url(self):
        '''切换当前url为下一页的url
           若下一页为空，则退出程序'''
        if self.next_page_url == '':
            pass
            # sys.exit()
        else:
            self.set_current_url(self.next_page_url)

    def is_finish(self):
        '''判断是否爬取完毕'''
        if self.current_page >= self.total_pages:
            return True
        else:
            return False

    def get_html(self):
        '''爬取当前url所指页面的内容，保存到html中'''
        r = requests.get(self.url, timeout=self.timeout, headers=self.headersParameters)
        if r.status_code == 200:
            self.html = r.text
            self.current_page += 1
        else:
            self.html = ''
            print('[ERROR]', self.url, 'get此url返回的http状态码不是200')

    def get_div_style(self):
        soup = BeautifulSoup(self.html, 'lxml')
        mc_set = []
        for i in range(1, 10):
            for j in range(1, 6):
                item_id = str(i) + '00' + str(j)
                item = soup.find('div', id=item_id)
                if item and item.h3.get_text():
                    mc_set.append(item.h3.get_text())
        return mc_set

    def get_urls(self):
        '''从当前html中解析出搜索结果的url，保存到o_urls'''
        o_urls = re.findall('href\=\"(http\:\/\/www\.baidu\.com\/link\?url\=.*?)\" class\=\"c\-showurl\"', self.html)
        o_urls = list(set(o_urls))  # 去重
        self.o_urls = o_urls
        # 取下一页地址
        next = re.findall(' href\=\"(\/s\?wd\=[\w\d\%\&\=\_\-]*?)\" class\=\"n\"', self.html)
        if len(next) > 0:
            self.next_page_url = 'https://www.baidu.com' + next[-1]
        else:
            self.next_page_url = ''

    def get_real(self, o_url):
        '''获取重定向url指向的网址'''
        r = requests.get(o_url, allow_redirects=False)  # 禁止自动跳转
        if r.status_code == 302:
            try:
                return r.headers['location']  # 返回指向的地址
            except:
                pass
        return o_url  # 返回源地址

    def transformation(self):
        '''读取当前o_urls中的链接重定向的网址，并保存到urls中'''
        self.urls = []
        for o_url in self.o_urls:
            self.urls.append(self.get_real(o_url))

    def print_urls(self):
        '''输出当前urls中的url'''
        for url in self.urls:
            print(url)

    def print_o_urls(self):
        '''输出当前o_urls中的url'''
        for url in self.o_urls:
            print(url)

    def run(self):
        h3_list = []
        while (not self.is_finish()):
            self.get_html()
            h3_list.extend(self.get_div_style())
            self.get_urls()
            self.transformation()
            # self.print_urls()
            self.switch_url()
        return h3_list


def crawler_brand(brand):
    h3_list = crawler(brand.encode("utf-8")).run()
    print(brand + "\t" + str(len(h3_list)))
    return h3_list


def save_data(data, save_path):
    with open(save_path, 'w+', encoding='utf-8') as f:
        for d in data:
            f.write(d + "\n")


if __name__ == '__main__':
    # params
    input_file_path = "search_words.txt"
    save_path = "search_words_thread_result.txt"
    start_time = time.time()
    # thread pool, default processes = cpu nums
    pool = Pool()
    brand_list = []
    with open(input_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            terms = line.strip().split("\t")
            brand_list.append(terms[0])

    # start from index
    index = 0
    for brand in brand_list[index:]:
        index += 1
        print("查询第%d个词：%s" % (index, brand))
        # 非阻塞式
        h3_list = pool.apply_async(crawler_brand, (brand,))
        # save data
        with open(save_path, 'a+', encoding='utf-8') as f:
            for d in h3_list.get():
                f.write(brand + "\t" + d + "\n")
    print("Start processes")
    pool.close()
    pool.join()
    print("Subprocess done.[spend_time:", time.time() - start_time, "]")  # [spend_time: 9.639744997024536 ]
