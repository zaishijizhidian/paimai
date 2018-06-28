# -*- coding: utf-8 -*-

from datetime import datetime

table_name = 'increment_data'
import pymysql
main_fields = ['item_id','bid_id', 'title','bid_status', 'applyCount', 'viewerCount', 'bidCount','itemUrl','dealPrice',
              'evaluatePrice','deal_time', 'deal_status','start_price','delay_count','court','contact',
               'phone_num', 'limit_status','remind_count','img_url', 'data_from','coordinate','latitude','longtitude','confidence','province', 'city',
               'town','detailAdrress','detail_desc','house_type','house_card_num','house_useage_detail',
               'create_time','edit_time','total_house_area','total_land_area','auction_people','jdu_doc_number','legal_remark','report_url']

class PaimaiPipeline(object):

    # 将数据存储到mysql
    def process_item(self, item, spider):
        item["crawled_time"] = datetime.now()
        item["spider"] = spider.name
        print("现在的时间：", item["crawled_time"])
        # logging.warning(item)
        self.conn = pymysql.connect(host='192.168.11.251', port=3306, user='root', password='youtong123', database='sipai', charset='utf8')
        self.cur = self.conn.cursor()

        sql = 'INSERT INTO {0}({1}) VALUES({2})'.format(table_name,','.join(main_fields),','.join(['%s'] * len(main_fields)))
        args = [item[k] for k in main_fields]
        arg = tuple(args)
        # print(arg)

        self.cur.execute(sql,arg)
        self.conn.commit()
        print("提交成功")
        # except:
        #     self.conn.rollback()
        # finally:
        self.cur.close()
        self.conn.close()
        print(item)
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
