# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import requests
from fake_useragent import UserAgent
from scrapy import signals
CHANGE_PROXY_STATUS_LIST = [404,302]

class ProxyMiddleware():
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    # def process_request(self, request,response,spider):
    #     # if request.meta.get('retry_times'):
    #     if response.status_code == 302:
    #         self.change_proxy()
            # if proxy:
            #     uri = 'https://{0}'.format(proxy)
            #     self.logger.debug('使用代理')
            #     request.meta['proxy'] = uri
            #     print(uri)

    def change_proxy(self,request):
        # if request.meta.get('retry_times'):
        proxy = self.get_random_proxy()
        if proxy:
            uri = 'https://{0}'.format(proxy)
            self.logger.debug('使用代理')
            request.meta['proxy'] = uri
            print(uri)
        return request

    def process_exception(self, item,response, exception, spider):
        if exception:
            self.logger.debug('error',item["item_url"] )

            # return_request = self.change_proxy(request)
            # if return_request:
            #     return return_request

    def process_response(self, request, response, spider):
        if response.status in CHANGE_PROXY_STATUS_LIST:
            return_request = self.change_proxy(request)
            if return_request:
                return return_request
        return response

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )


class RandomUserAgentMiddlware(object):
    #随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())





