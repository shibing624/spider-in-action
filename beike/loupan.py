# coding=utf-8
# 获得指定城市的所有新房楼盘数据
import sys

sys.path.append("../")
from beike.core.loupan_spider import LouPanBaseSpider
from beike.config import SPIDER_NAME

if __name__ == "__main__":
    spider = LouPanBaseSpider(SPIDER_NAME)
    spider.start()
