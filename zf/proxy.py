# -*-coding:utf-8-*-  

import logging
import requests
import random

logger = logging.getLogger(__name__)

class DownloadProxyMiddleware(object):
    def __init__(self):
        logger.info('Proxy Middleware has been started')
        self.proxy_pool = [self.get_proxy().decode('utf-8') for i in range(10)]

    def get_proxy(self):
        return requests.get('http://127.0.0.1:5010/get/').content

    def delete_proxy(self, proxy):
        requests.get('http://127.0.0.1:5010/delete/?proxy={}'.format(proxy))
        if proxy in self.proxy_pool:
            self.proxy_pool.remove(proxy)
            logger.info("Delete proxy {}".format(proxy))
            self.proxy_pool.append(self.get_proxy())

    def process_request(self, request, spider):
        #if 'main' in request.meta.keys() and 'redirect_urls' not in request.meta.keys():
        #if 'need_proxy' in request.meta.keys() and request.meta['need_proxy']:
            #proxy = self.get_proxy().decode('utf-8')
            #logger.info('Proxy using http://{}'.format(proxy))
        if 'item' not in request.meta.keys() and 'redirect_urls' not in request.meta.keys():
            proxy = random.choice(self.proxy_pool)
            logger.info("Using proxy {}".format(proxy))
            request.meta['proxy'] = "http://{}".format(proxy)

        if 'retry_times' in request.meta.keys() and 'proxy' in request.meta.keys():
            logger.debug("retry proxy {}".format(request.meta['proxy']))
            self.delete_proxy(request.meta['proxy'][:7])

        return None
