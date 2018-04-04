# -*- coding: utf-8 -*-
import scrapy
import httplib2
from scrapy.selector import Selector
import requests
import redis

from zf.items import ZfItem


def got_data(tmp_list, default="None"):
    if tmp_list:
        return tmp_list[0]
    else:
        return default

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["hz.lianjia.com/zufang/", "restapi.amap.com"]
    start_urls = (
        #'http://www.hz.lianjia.com/zufang/pg{}'.format(i) for i in range(1, 100)
        'http://hz.lianjia.com/zufang/pg{}'.format(pg) for pg in range(1,101)
    )

    def __init__(self, *args):
        super(LianjiaSpider, self).__init__(*args)
        self.redis_pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)

    def start_requests(self):
        requests = [scrapy.FormRequest(url) for url in self.start_urls]
        for request in requests:
            request.meta['main'] = True
        return requests
        

    def parse(self, response):
        try:
            sel_hl = response.xpath("//ul[contains(@id, 'house-lst')]")[0]
        except Exception:
            self.log("CAN'T PRASE")
            return

        if sel_hl.xpath("./li[@class='list-no-data clear']"):
            self.log("Request {} has been blocked down".format(response.url))
            return

        for sel_li in sel_hl.xpath(".//li"):
            item = ZfItem()

            item['descript'] = got_data(sel_li.xpath("//div[@class='info-panel']/h2//text()").extract())
            item['id'] = got_data(sel_li.xpath("./@data-id").extract())
            item['xiaoqu_link'] = got_data(sel_li.xpath(".//div[contains(@class, 'where')]/a/@href").extract())
            item['xiaoqu_name'] = got_data(sel_li.xpath(".//span[contains(@class, 'region')]/text()").extract()).strip()
            item['zone'], item['meters'], item['orient'] = ( s.strip() for s in sel_li.xpath(".//div[contains(@class, 'where')]/span//text()").extract() )
            item['high'], item['year'] = ( sel_li.xpath(".//div[contains(@class, 'other')]//text()").extract()[i] for i in [-3,-1] )
            item['price'], tmp, item['price_update'] = ( s.strip() for s in sel_li.xpath(".//div[contains(@class, 'price')]//text()").extract() )
            item['price'] += tmp

            r = redis.Redis(connection_pool=self.redis_pool)
            value = r.get(item['xiaoqu_name'])
            if not value:
                url_location = u"http://restapi.amap.com/v3/geocode/geo?address=杭州{}&output=XML&key=***".format(item['xiaoqu_name'])
                request = scrapy.Request(url_location, callback=self.gaode_location_parse)
                request.meta['item'] = item
                yield request
            else:
                item['location'] = value
                yield item

        

    def gaode_location_parse(self, response):
        item = response.meta['item']
        item['location'] = got_data(response.xpath("//location/text()").extract())
        #TODO: item down
        r = redis.Redis(connection_pool=self.redis_pool)
        r.set(item['xiaoqu_name'], item['location'])
        self.log("SAVE xiaoqu:{} location:{}".format(item['xiaoqu_name'], item['location']))
        yield item

