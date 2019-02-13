# coding=utf-8
# 获得指定城市的出租房数据

from beike.core.zufang_spider import ZuFangBaseSpider
from beike.config import SPIDER_NAME

if __name__ == "__main__":
    spider = ZuFangBaseSpider(SPIDER_NAME)
    spider.start()
