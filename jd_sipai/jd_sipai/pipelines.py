# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



from datetime import datetime

from retrying import retry

table_name1 = 'increment_data'
# table_name2 = 'bid_test_info'
import pymysql
# main_fields = ['item_id', 'bid_id', 'title', 'bid_status', 'applyCount', 'viewerCount', 'bidCount', 'itemUrl',
#                'dealPrice','evaluatePrice', 'deal_time', 'deal_status', 'start_price', 'court', 'contact',
#                'phone_num', 'limit_status', 'img_url', 'data_from', 'province',
#                'city', 'town', 'detailAdrress', 'detail_desc']
main_fields = ['item_id','bid_id', 'title','bid_status', 'applyCount', 'viewerCount', 'bidCount','itemUrl','dealPrice',
              'evaluatePrice','deal_time', 'deal_status','start_price','delay_count','court','contact',
               'phone_num', 'limit_status','img_url', 'data_from','coordinate','latitude','longtitude',
               'confidence','province', 'city', 'town','detailAdrress','detail_desc','house_useage_detail','create_time','edit_time']


# main_fields2 = ['paimaiId','bid_code','bid_record_time','bid_record_price','bid_record_status']

class JdSipaiPipeline(object):
    # @retry(stop_max_attempt_number=4)
    def process_item(self, item, spider):
        item["crawled_time"] = datetime.now()
        item["spider"] = spider.name
        # print("现在的时间：", item["crawled_time"])
        # logging.warning(item)
        self.conn = pymysql.connect(host='192.168.11.251',
                                    port=3306,
                                    user='root',
                                    password='youtong123',
                                    database='sipai',
                                    charset='utf8')
        self.cur = self.conn.cursor()

        sql1 = 'INSERT INTO {0}({1}) VALUES({2})'.format(table_name1, ','.join(main_fields),','.join(['%s'] * len(main_fields)))
        args1 = [item[k] for k in main_fields]
        arg1 = tuple(args1)
        # print(arg)
        self.cur.execute(sql1, arg1)
        self.conn.commit()
        # print(item["item_id"],"-------")
        print("提交成功")
        self.cur.close()
        self.conn.close()
        # print(item)
        return item
