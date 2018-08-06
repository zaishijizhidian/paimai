
from datetime import datetime

# table_name = 'increment_data'
table_name = 'sm_court'
import pymysql
main_fields = ['court', 'address', 'phone_num']

class CourtPipeline(object):
    # 将数据存储到mysql
    def process_item(self, item, spider):
        item["crawled_time"] = datetime.now()
        item["spider"] = spider.name
        print("现在的时间：", item["crawled_time"])
        # logging.warning(item)
        self.conn = pymysql.connect(host='192.168.11.251',
                                    port=3306,
                                    user='root',
                                    password='youtong123',
                                    database='sipai',
                                    charset='utf8')
        self.cur = self.conn.cursor()

        sql = 'INSERT INTO {0}({1}) VALUES({2})'.format(table_name, ','.join(main_fields),','.join(['%s'] * len(main_fields)))
        args = [item[k] for k in main_fields]
        arg = tuple(args)
        self.cur.execute(sql, arg)
        self.conn.commit()
        print("提交成功")
        self.cur.close()
        self.conn.close()
        print(item)
        # return item

