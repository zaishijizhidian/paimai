# -*- coding: utf-8 -*-

# Scrapy settings for court project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'court'

SPIDER_MODULES = ['court.spiders']
NEWSPIDER_MODULE = 'court.spiders'



ITEM_PIPELINES = {
   'court.pipelines.CourtPipeline': 300,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'court (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

#设置自动限速，防止爬去过快出现数据的遗漏
# AUTOTHROTTLE_ENABLED = True
#自动限速1秒
# AUTOTHROTTLE_START_DELAY = 1

#日志设置
LOG_FILE = './court.log'
LOG_LEVEL = "WARNING"


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
'Cookie':'userSelectCity=hangzhou; areaInfo=0XfPn5QEJpsyUE%2B94tMxwdUbO4UgveLGKkpfz%2F460mglmsSxiXOd6CH6GKSza7vjjVElZ2Wyu57TyPMKqdP8xrCDgX4CWZBySRk4bX4; uuid=DhF5WFsfabgXKCH8CKiPAg==; product_areaInfo=13jInsMCdM4yUFarr59qnYZPVNR%2B%2BvPMK1dTg%2BYywjB0xJPnw3%2BBvnSHCaS5fLHiilElZ3VmPjYFSUAK5p7qwbCI2htBzWi%2Bz8HCKiEIHG2P; PHPSESSID=sjo0ag20vlbtdfere84kblj422; Hm_lvt_ab3790496cb8e9723320f258938d16d3=1528785337,1530607714,1530668885,1530758126; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; Hm_lpvt_ab3790496cb8e9723320f258938d16d3=1530771163',
'Host': 'www.lawtime.cn',
'Referer': 'http://www.lawtime.cn/fayuan/city/tianjin',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'court.middlewares.CourtSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'court.middlewares.ProxyMiddleware': 543,
   'court.middlewares.UserAgentMiddleware': 100
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
