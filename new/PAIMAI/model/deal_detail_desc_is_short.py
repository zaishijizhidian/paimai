# -*- coding: utf-8 -*-
import datetime
import json
import re
from multiprocessing.pool import ThreadPool

import pymysql
from lxml import etree

import requests

"""
对于详情描述小于50的情况，直接获取拍卖公告的信息
"""

def get_detail_desc(url):
    # 获取json文本，转化成element对象
    response = requests.get(url)
    # 详情字段为空时，提取拍卖公告中的数据
    res = etree.HTML(response.text)
    detail_desc_temp = res.xpath("//*//text()")
    if detail_desc_temp:
        # print(detail_desc_temp)
        detail_desc_1 = ','.join(detail_desc_temp).strip()
        ds = re.sub('\s', '', detail_desc_1).replace(',', '')
        detail_desc_text2 = re.search(r"一、(.*?)二、", ds)
        if detail_desc_text2:
            detail_desc2 = ','.join(detail_desc_text2.group(1)).strip()
            ds = re.sub('\s', '', detail_desc2).replace(',', '').replace('、', '')
            return ds