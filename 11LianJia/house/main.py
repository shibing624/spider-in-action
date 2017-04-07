# - * - coding: utf-8 - * -
# 运行前打开redis和mongo服务
from scrapy import cmdline
cmdline.execute("scrapy crawl house".split())