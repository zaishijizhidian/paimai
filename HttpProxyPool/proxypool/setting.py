
#阿里云redis接口(host='116.62.190.193', port=6379,password='123456', db=1)
# Redis数据库地址
REDIS_HOST = '116.62.190.193'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = 123456

REDIS_KEY = 'proxies'
#选取redis的第三个库
DB = 3
# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

VALID_STATUS_CODES = [200, 300]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 50000

# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 300

# 测试API，建议抓哪个网站测哪个
# TEST_URL = 'http://www.baidu.com'
TEST_URL = 'https://sf.taobao.com/item_list.htm'

# API配置
API_HOST = '0.0.0.0'
API_PORT = 5555

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 100
