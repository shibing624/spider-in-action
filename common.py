# -*- coding: utf-8 -*-
"""
@description: 爬虫通用操作类
@author:XuMing
"""
from __future__ import print_function  # 兼容python3的print写法
from __future__ import unicode_literals  # 兼容python3的编码处理

import cookielib
import logging
import os
import re
import urllib
import urllib2


class Common(object):
    def __init__(self):
        # init params
        self.url_path = None
        self.post_data = None
        self.header = {}
        self.domain = None
        self.operate = None
        self.logger = None
        # init cookie
        self.cookie_jar = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie_jar))
        urllib2.install_opener(self.opener)

    def set_request_data(self, url_path=None, post_data=None, header=None):
        self.url_path = url_path
        self.post_data = post_data
        self.header = header

    def send_request(self, url, data={}, header={}):
        request = urllib2.Request(url, urllib.urlencode(data), header)
        result = urllib2.urlopen(request)
        return result

    def get_html_text(self, is_cookie=False):
        if self.post_data == None and self.header == {}:
            request = urllib2.Request(self.url_path)
        elif self.post_data == None:
            request = urllib2.Request(self.url_path, headers=self.header)
        else:
            request = urllib2.Request(self.url_path, urllib.urlencode(self.post_data), self.header)
        result = urllib2.urlopen(request)
        if is_cookie:
            self.operate = self.opener.open(request)
        return result.read()

    def save_captcha(self, captcha_url, out_path, save_mode='wb'):
        # 用opener访问验证码地址,获取cookie
        picture = self.opener.open(captcha_url).read()
        # self.mkdirs(out_path)
        local = open(out_path, save_mode)
        local.write(picture)
        local.close()

    def get_html(self, url):
        page = urllib.urlopen(url)
        html = page.read()
        return html

    # 功能：将文本内容输出至本地
    def output(self, content, out_path, save_mode="w"):
        # self.mkdirs(out_path)
        fw = open(out_path, save_mode)
        fw.write(content)
        fw.close()

    def create_logger(self, logger_name, log_file):
        # self.mkdirs(log_file)
        # 创建一个logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_file)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        # 定义handler的输出格式formatter
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)
        self.logger = logger
        return logger

    # 创建新目录
    def mkdir(self, path):
        path = path.strip()
        if not os.path.exists(path):
            os.makedirs(path)

    def mkdirs(self, path):
        prefix = os.path.dirname(path)
        if not os.path.exists(prefix):
            os.makedirs(prefix)

    # 在html中解析重定位结果部分函数
    def redirect_data(self, text):
        p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
        login_url = p.search(text).group(1)
        return login_url
