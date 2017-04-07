# -*- coding: utf-8 -*-

# Scrapy settings for house project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'house'

SPIDER_MODULES = ['house.spiders']
NEWSPIDER_MODULE = 'house.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'house (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 调度
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  # 去重
SCHEDULER_PERSIST = True  # 不清理Redis队列
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"  # 队列

ITEM_PIPELINES = {
    'house.pipelines.HousePipeline': 300,
}

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = "lianjia"
MONGODB_DOCNAME = "house_info_2"
COOKIES_DEBIG=True
