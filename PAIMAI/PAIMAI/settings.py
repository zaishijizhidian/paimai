# -*- coding: utf-8 -*-



BOT_NAME = 'PAIMAI'

SPIDER_MODULES = ['PAIMAI.spiders']
NEWSPIDER_MODULE = 'PAIMAI.spiders'

#指定去重队列
# SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
#持久化去重
# SCHEDULER_PERSIST = False
#指定去重方法给request对象去重
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

ITEM_PIPELINES = {
   'PAIMAI.pipelines.PaimaiPipeline': 300,
   # 'PAIMAI.pipelines.MongoDBPipeline': 301,

    # 'scrapy_redis.pipelines.RedisPipeline':400,
}

# MONGO_HOST = "10.50.86.170"  # 主机IP
MONGO_HOST = "10.50.86.179"  # 主机IP
MONGO_PORT = 27017  # 端口号
# MONGO_DB = "yt_spider"  # 库名
MONGO_DB = "dw"  # 库名
MONGO_COLL = "sipai"  # collection名
# MONGO_USER = "ytuser"
MONGO_USER = "dpuser"
# MONGO_PSW = "DpVsSGTcCUfj4532"
MONGO_PSW = "HxSwQT3AIPwMkIaD"



ROBOTSTXT_OBEY = False
# REDIS_URL = "reids://127.0.0.1:6379"

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

#设置自动限速，防止爬去过快出现数据的遗漏
# AUTOTHROTTLE_ENABLED = True
#自动限速1秒
# AUTOTHROTTLE_START_DELAY = 1

#日志设置
LOG_FILE = './bid_over.log'
LOG_LEVEL = "WARNING"




# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'PAIMAI (+http://www.yourdomain.com)'

# Obey robots.txt rules

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1
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
#    'PAIMAI.middlewares.PaimaiSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'PAIMAI.middlewares.MyCustomDownloaderMiddleware': 543,
#}

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
