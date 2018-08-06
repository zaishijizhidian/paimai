# -*- coding: utf-8 -*-
#用于调试SCRAPY
import os

from scrapy.cmdline import execute

import sys



sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#打印出当前代码所在的目录
# print(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","lawyer"])
















