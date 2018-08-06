# -*- coding: utf-8 -*-
import pymysql

filename = './data.txt'

main_fields = ['uuid', 'bid_id', 'create_date', 'update_date', 'court', 'contacts', 'phone_num', 'asset_name',
               'asset_address', 'longitude', 'latitude', 'asset_type', 'asset_no',
               'evaluate_price', 'starting_price', 'deal_price', 'report_no', 'asset_holders', 'case_no', 'trade_date',
               'auction_type',
               'auction_status', 'legal_remark', 'asset_des', 'province', 'city', 'source_name', 'source_url',
               'coordniate']

table_name = 'sm_auction'


class update_data:
    def __init__(self):
        self.conn = pymysql.connect(  # host='localhost',
            host='192.168.11.251',
            port=3306,
            user='root',
            password='youtong123',
            # password='mysql',
            database='sipai',
            charset='utf8')
        # )  # 默认返回元祖，加上这个参数返回的是字典结构
        # self.conn = pymysql.connect(host='data.npacn.com', port=3306, user='youtong', password='duc06LEQpgoP',
        #                        database='sipai', charset='utf8')

    def write_id(self):
        conn = self.conn
        with conn.cursor() as cur1:
            # sql1 = "SELECT id,title from land_sum_info a WHERE a.confidence is not Null;"
            # sql1 = "SELECT id,trade_date,deal_price,auction_status FROM `test_increment_sm_auction` limit 10;"
            sql1 = "SELECT id,bid_id FROM `sm_auction`;"
            cur1.execute(sql1)
            # 设定游标从第一个开始移动
            cur1.scroll(0, mode='absolute')
            # 获取此字段的所有信息
            f = open(filename, 'a')
            results = cur1.fetchall()
            # print(results)
            for result in results:
                id = str(result[1])
                f.write(id + '\n')
            f.close()
            conn.commit()
            conn.cursor().close()
            print("**" * 50)

    def update_id(self):
        conn = self.conn
        with conn.cursor() as cur1:
            # sql1 = "SELECT id,title from land_sum_info a WHERE a.confidence is not Null;"
            # sql1 = "SELECT id,trade_date,deal_price,auction_status FROM `test_increment_sm_auction` limit 10;"
            # 直接在增量数据increment_data中提取数据
            sql1 = "SELECT * FROM `increment_data`;"
            # sql1 = "SELECT * FROM `increment_data_jd`;"
            cur1.execute(sql1)
            # 设定游标从第一个开始移动
            cur1.scroll(0, mode='absolute')
            # 获取此字段的所有信息
            with open(filename, 'r') as f:
                id_list = list(set([line.strip() for line in f.readlines()]))
                # print(id_list)
                results = cur1.fetchall()
                # print(results)
                item = {}
                n = 0
                for result in results:
                    item["uuid"] = str(result[1])
                    item["bid_id"] = str(result[2])
                    item["asset_name"] = result[3]
                    item["auction_type"] = result[4]
                    item["source_url"] = result[8]
                    item["deal_price"] = result[9]
                    item["evaluate_price"] = result[10]
                    item["trade_date"] = result[11]
                    item["auction_status"] = result[12]
                    item["starting_price"] = result[13]
                    item["court"] = result[15]
                    item["contacts"] = result[16]
                    item["phone_num"] = result[17]
                    item["source_name"] = result[21]
                    item["coordniate"] = result[22]
                    item["latitude"] = result[23]
                    item["longitude"] = result[24]
                    item["province"] = result[26]
                    item["city"] = result[27]
                    item["asset_address"] = result[29]
                    item["asset_des"] = result[30]
                    item["asset_type"] = result[31]
                    item["asset_no"] = result[32]
                    item["create_date"] = result[34]
                    item["update_date"] = result[35]
                    item["asset_holders"] = result[38]
                    item["case_no"] = result[39]
                    item["legal_remark"] = result[40]
                    item["report_no"] = result[41]
                    # item["uuid"] = str(result['item_id'])
                    # item["bid_id"] = str(result['bid_id'])
                    # item["create_date"] = str(result['create_time'])
                    # item["edit_date"] = str(result['edit_time'])
                    # item["court"] = result['court']
                    # item["contacts"] = result['contact']
                    # item["phone_num"] = result['phone_num']
                    # item["asset_name"] = result['title']
                    # item["asset_address"] = result['detailAdrress']
                    # item["longitude"] = result['longtitude']
                    # item["latitude"] = result['latitude']
                    # item["asset_type"] = result['house_type']
                    # item["asset_no"] = result['house_card_num']
                    # item["evaluate_price"] = result['evaluatePrice']
                    # item["starting_price"] = result['start_price']
                    # item["deal_price"] = result['dealPrice']
                    # item["report_no"] = result['report_url']
                    # item["asset_holders"] = result['auction_people']
                    # item["case_no"] = result['jdu_doc_number']
                    # item["trade_date"] = result['deal_time']
                    # item["auction_type"] = result['bid_status']
                    # item["auction_status"] = result['deal_status']
                    # item["legal_remark"] = result['legal_remark']
                    # item["asset_des"] = result['detail_desc']
                    # item["province"] = result['province']
                    # item["city"] = result['city']
                    # item["source_name"] = result['data_from']
                    # item["source_url"] = result['itemUrl']
                    # item["coordniate"] = result['coordinate']
                    # print(item)
                    #
                    # #
                    #     #如果id 不在列表中，直接写入文件，并插入新增的数据
                    if item["bid_id"] not in id_list:
                        f = open(filename, 'a')
                        f.write(item["bid_id"] + '\n')
                        f.close()

                        with conn.cursor() as cur2:
                            sql = 'INSERT INTO {0}({1}) VALUES({2})'.format(table_name, ','.join(main_fields),
                                                                            ','.join(['%s'] * len(main_fields)))
                            args = [item[k] for k in main_fields]
                            arg = tuple(args)
                            cur2.execute(sql, arg)
                            conn.commit()
                            conn.cursor().close()
                            n += 1
                            print("第%d条插入成功" % (n))
                    # 如果在列表中，就更新最新的数据
                    else:
                        with conn.cursor() as cur2:
                            # "insert into test_increment_sm_auction (id, name, age) values(1, "A", 19) on duplicate key update name=values(name), age=values(age)"
                            sql2 = 'update sm_auction set create_date = %s,update_date = %s, deal_price = %s,trade_date = %s,auction_type = %s,auction_status = %s where bid_id = %s'
                            cur2.execute(sql2, (
                                item["create_date"], item["update_date"], item["deal_price"], item["trade_date"],
                                item["auction_type"], item["auction_status"], item["bid_id"]))
                            conn.commit()
                            conn.cursor().close()
                            n += 1
                        print("第%d条更新成功" % (n))

        with conn.cursor() as cur2:  # 将增量数据存入总量数据库

            sql = "INSERT into increment_data_180628 SELECT * from increment_data;" #只能插入到一个空表中，如果两个表都有主键id，会造成主键冲突
            cur2.execute(sql)
            conn.commit()
            conn.cursor().close()
        with conn.cursor() as cur3:  # 将增量数据库清空
            sql = "DELETE FROM `increment_data`;"
            cur3.execute(sql)
            conn.commit()
            conn.cursor().close()

if __name__ == '__main__':
    update_data = update_data()
# update_data.write_id()
    update_data.update_id()
