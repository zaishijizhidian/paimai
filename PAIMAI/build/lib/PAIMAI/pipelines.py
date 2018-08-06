# -*- coding: utf-8 -*-

from datetime import datetime

import pandas as pd
import redis
# table_name = 'increment_data'
from scrapy.exceptions import DropItem

table_name = 'increment_data'
import pymysql
main_fields = ['item_id','bid_id', 'title','bid_status', 'applyCount', 'viewerCount', 'bidCount','itemUrl','dealPrice',
              'evaluatePrice','deal_time', 'deal_status','start_price','delay_count','court','contact',
               'phone_num', 'limit_status','remind_count','img_url', 'data_from','coordinate','latitude','longtitude','confidence','province', 'city',
               'town','detailAdrress','detail_desc','house_type','house_card_num','house_useage_detail',
               'create_time','edit_time','total_house_area','total_land_area','auction_people','jdu_doc_number','legal_remark','report_url']

redis_db = redis.Redis(host='127.0.0.1', port=6379, db=4)  # 连接redis，相当于MySQL的conn
redis_data_dict = "f_url"

class PaimaiPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='192.168.11.251', port=3306, user='root', password='youtong123', database='sipai', charset='utf8')
        redis_db.flushdb()  # 删除全部key，保证key为0，不然多次运行时候hlen不等于0，刚开始这里调试的时候经常出错。
        if redis_db.hlen(redis_data_dict) == 0:  #
            # sql = "SELECT source_url FROM sm_auction;"  # 从你的MySQL里提数据，我这里取url来去重。
            sql = "SELECT itemUrl FROM increment_data;"  # 从你的MySQL里提数据，我这里取url来去重。
            df = pd.read_sql(sql, self.conn)  # 读MySQL数据
            for url in df['itemUrl'].get_values():  # 把每一条的值写入key的字段里
                redis_db.hset(redis_data_dict, url, 0)

    # 将数据存储到mysql
    def process_item(self, item, spider):
        conn = pymysql.connect(host='192.168.11.251', port=3306, user='root', password='youtong123', database='sipai',charset='utf8')
        if redis_db.hexists(redis_data_dict, item['itemUrl']):  # 取item里的url和key里的字段对比，看是否存在，存在就丢掉这个item。不存在返回item给后面的函数处理
            raise DropItem("Duplicate item found: %s" % item)
        item["crawled_time"] = datetime.now()
        item["spider"] = spider.name
        print("现在的时间：", item["crawled_time"])
        cur = conn.cursor()

        sql = 'INSERT INTO {0}({1}) VALUES({2})'.format(table_name,','.join(main_fields),','.join(['%s'] * len(main_fields)))
        args = [item[k] for k in main_fields]
        arg = tuple(args)
        # print(arg)

        cur.execute(sql,arg)
        conn.commit()
        print("提交成功")
        cur.close()
        conn.close()
        # print(item)
        return item



    # def __init__(self):
    #     # 链接数据库, 数据库登录需要帐号密码的话
    #     self.client = pymongo.MongoClient('mongodb://{0}:{1}@{2}:{3}'.format(settings.MONGO_USER,settings.MONGO_PSW,settings.MONGO_HOST,settings.MONGO_PORT))
    #     self.db = self.client[settings.MONGO_DB]  # 获得数据库的句柄
    #     self.coll = self.db[settings.MONGO_COLL]  # 获得collection的句柄
    # #将数据存储到mongodb
    # def process_item(self, item, spider):
    #     postItem = dict(item)  # 把item转化成字典形式
    #     self.coll.insert(postItem)  # 向数据库插入一条记录
    #     return item  # 会在控制台输出原item数据，可以选择不写
