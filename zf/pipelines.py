# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis
import logging

logger = logging.getLogger(__name__)


class LianjiaPipeline(object):
    def __init__(self):
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        self.con = redis.Redis(connection_pool=pool)
        logger.info("Open redis pool")

    def process_item(self, item, spider):
        lianjia_name = "lianjia_{}".format(item["id"])
        del item["id"]
        self.con.hmset(lianjia_name, item)
        return item
