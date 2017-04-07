# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

from .items import HouseItem


class HousePipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[db_name]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        if isinstance(item, HouseItem):
            try:
                info = dict(item)
                if self.post.insert(info):
                    print('insert ok')
            except Exception:
                pass
        return item
