# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""

thread_pool_size = 50

# 防止爬虫被禁，随机延迟设定
# 如果不想delay，就设定False，
# 具体时间可以修改random_delay()，由于多线程，建议数值大于10
RANDOM_DELAY = False

proxy_url = "http://www.xicidaili.com/nt/1"
SPIDER_NAME = "ke"
start_url = "http://www.ke.com"
log_path = "log.txt"
