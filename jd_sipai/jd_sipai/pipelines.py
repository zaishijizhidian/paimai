# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



from datetime import datetime

from retrying import retry

table_name = 'increment_data_jd'
# table_name2 = 'bid_test_info'
import pymysql
# main_fields = ['item_id', 'bid_id', 'title', 'bid_status', 'applyCount', 'viewerCount', 'bidCount', 'itemUrl',
#                'dealPrice','evaluatePrice', 'deal_time', 'deal_status', 'start_price', 'court', 'contact',
#                'phone_num', 'limit_status', 'img_url', 'data_from', 'province',
#                'city', 'town', 'detailAdrress', 'detail_desc']
main_fields = ['item_id','bid_id', 'title','bid_status', 'applyCount', 'viewerCount', 'bidCount','itemUrl','dealPrice',
              'evaluatePrice','deal_time', 'deal_status','start_price','delay_count','court','contact',
               'phone_num', 'limit_status','remind_count','img_url', 'data_from','coordinate','latitude','longtitude',
               'confidence','province', 'city','town','detailAdrress','detail_desc','house_type','house_card_num',
               'house_useage_detail','create_time','edit_time','total_house_area','total_land_area','auction_people',
               'jdu_doc_number','legal_remark','report_url']


# main_fields2 = ['paimaiId','bid_code','bid_record_time','bid_record_price','bid_record_status']

class JdSipaiPipeline(object):

    def process_item(self, item, spider):
        conn = pymysql.connect(host='data.npacn.com', port=3306, user='youtong', password='duc06LEQpgoP', database='sipai',charset='utf8')

        item["crawled_time"] = datetime.now()
        item["spider"] = spider.name
        print("现在的时间：", item["crawled_time"])
        # print(111)
        cur = conn.cursor()
        # print(222)
        sql = 'INSERT INTO {0}({1}) VALUES({2})'.format(table_name,','.join(main_fields),','.join(['%s'] * len(main_fields)))
        args = [item[k] for k in main_fields]
        arg = tuple(args)
        # print(arg)

        cur.execute(sql,arg)
        conn.commit()
        print("提交成功")
        cur.close()
        conn.close()
        print(item)
        # return item