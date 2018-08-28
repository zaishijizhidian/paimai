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
# MONGO_HOST = "10.50.86.179"  # 主机IP
# MONGO_PORT = 27017  # 端口号
# MONGO_DB = "yt_spider"  # 库名
# MONGO_DB = "dw"  # 库名
# MONGO_COLL = "sipai"  # collection名
# MONGO_USER = "ytuser"
# MONGO_USER = "dpuser"
# MONGO_PSW = "DpVsSGTcCUfj4532"
# MONGO_PSW = "HxSwQT3AIPwMkIaD"



ROBOTSTXT_OBEY = False
# REDIS_URL = "reids://127.0.0.1:6379"


#设置自动限速，防止爬去过快出现数据的遗漏
# AUTOTHROTTLE_ENABLED = True
#自动限速1秒
# AUTOTHROTTLE_START_DELAY = 1

#日志设置
# LOG_FILE = '../bid_over.log'
# LOG_LEVEL = "WARNING"

PROXY_URL = 'http://localhost:5555/random'

RANDOM_UA_TYPE = "random"

RETRY_HTTP_CODES = [302,401,403,408,414,500,502,503,504]

DOWNLOADER_MIDDLEWARES = {
   'PAIMAI.middlewares.ProxyMiddleware': 543,
   # 'PAIMAI.middlewares.RandomUserAgentMiddlware': 542
   'scrapy.downloadermiddlewares.retry.RetryMiddleware':None
}



# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'PAIMAI (+http://www.yourdomain.com)'

# Obey robots.txt rules

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.25
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
   'accept-encoding': 'gzip, deflate, br',
   'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
   'cache-control': 'max-age=0',
   # 'cookie': 't=91e0c7185ddf7ca1a711e17489e4b59b; cna=/D/LE+x6kQ8CAXPMaRTe4Nht; tg=0; l=Ap2drM46-HVs1gaJTleSaMOnLXKWzNEK; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; enc=i1qAwx%2FeCzSSirdI84hhhaKJdlcG9djuUxh8e2pO9QdYXA2G6xsh%2FGy%2BAMmyDP8TjroLER71l7sPY6O0LAaQ0Q%3D%3D; v=0; cookie2=12d1715fd3d6ccfa8904ead1e29bf948; _tb_token_=53eae8f7fb365; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; unb=1080233313; sg=n37; _l_g_=Ug%3D%3D; skt=d39ed32a9a7dcb6b; cookie1=BYXJ5loYhwf%2BmBb5L8YBMhLcvcSlV46AvTfzJs3HLCI%3D; csg=ec8d0dfc; uc3=vt3=F8dBzrtoT5Kx2oEa56I%3D&id2=UoH38y9PhsfN%2Bw%3D%3D&nk2=GckzvrBWD8YmNFNcxmkL&lg2=W5iHLLyFOGW7aA%3D%3D; existShop=MTUzNTAxNjEzOA%3D%3D; tracknick=zaishijizhidian; lgc=zaishijizhidian; _cc_=URm48syIZQ%3D%3D; dnk=zaishijizhidian; _nk_=zaishijizhidian; cookie17=UoH38y9PhsfN%2Bw%3D%3D; mt=ci=0_1; swfstore=192069; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; uc1=cookie14=UoTfLi2Izm%2BSrw%3D%3D&lng=zh_CN&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&existShop=false&cookie21=VFC%2FuZ9ainBZ&tag=8&cookie15=VT5L2FSpMGV7TQ%3D%3D&pas=0; isg=BFNThye-DAQap8DSOvURxSmv4te9oOWa7tIx4QVw5HKqhHMmjdqhGpzWurRPJD_C; whl=-1%260%260%261535019939059',
   'referer': 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fsf.taobao.com%2Fitem_list.htm%3Fspm%3Da213w.3064813.a214dqe.1.55B4Xj',
   'upgrade-insecure-requests': 1,
   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

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
