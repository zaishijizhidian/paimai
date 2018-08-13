# -*- coding: utf-8 -*-

# Scrapy settings for jd_sipai project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import datetime

import redis

BOT_NAME = 'jd_sipai'

SPIDER_MODULES = ['jd_sipai.spiders']
NEWSPIDER_MODULE = 'jd_sipai.spiders'

#指定去重队列
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
#持久化去重
SCHEDULER_PERSIST = True

#指定去重方法给request对象去重 去重规则对应处理的类
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 默认使用优先级队列（默认广度优先），其他：PriorityQueue（有序集合），FifoQueue（列表）、LifoQueue（列表）
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'

# 对保存到redis中的数据进行序列化，默认使用pickle
SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"

# 是否在开始之前清空 调度器和去重记录，True=清空，False=不清空
SCHEDULER_FLUSH_ON_START = False
# 去重规则，在redis中保存时对应的key
SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'

ITEM_PIPELINES = {
   'jd_sipai.pipelines.JdSipaiPipeline': 300,
    # 'scrapy_redis.pipelines.RedisPipeline':400,
}

DUPEFILTER_DEBUG = False

ROBOTSTXT_OBEY = False

#构造redis_url地址．密码前面以：开头，以库名结尾
REDIS_URL = "reids://:123456@116.62.190.193:6379"
#自定义的redis参
# REDIS_HOST = '116.62.190.193'
# REDIS_PORT = 6379
# REDIS_PASSWORD  = '123456'

# REDIS_PARAMS['redis_cls']= redis.Redis(host='116.62.190.193', port=6379,password='123456', db=0)

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'


startDate = datetime.datetime.now().strftime('%Y%m%d')
# LOG_FILE=f"mySpiderlog{startDate}.txt"
LOG_FILE = './jd_sipai{}.txt'.format(startDate)
LOG_LEVEL = "WARNING"

REDIS_ENCODING = "utf-8"

REDIS_START_URLS_BATCH_SIZE = 1

# 把起始url放到redis的列表
REDIS_START_URLS_AS_SET = False

#设置自动限速，防止爬去过快出现数据的遗漏
AUTOTHROTTLE_ENABLED = True
#自动限速1秒
AUTOTHROTTLE_START_DELAY = 1

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jd_sipai (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = False

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
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'jd_sipai.middlewares.JdSipaiSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'jd_sipai.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'jd_sipai.pipelines.JdSipaiPipeline': 300,
#}

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
