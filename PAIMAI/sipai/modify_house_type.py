# -*- coding: utf-8 -*-
import pymysql


def modify_type(str):
    list1 = ['住宅','住房','房屋','房产','公寓','含车位','别墅','单元','苑','小区','房地产','幢']
    list2 = ['办公','写字楼','商办','商务','商住','商务中心','国贸']
    list3 = ['商铺','商服','商网','商贸','商城','市场','商场','营业','商业','门面','门点','铺位','铺面','底商','店铺','门店','门市','酒店','店面']
    list4 = ['车库','车位','地下室','停车场','车房','储藏室']
    list5 = ['土地','使用权','林地','用地','亩']
    list6 = ['建筑物','厂房','工业','附着物','在建工程']
    type = None
    for str2 in list1:
        if str.rfind(str2)>=0:
             type = '01'
    for str2 in list2:
        if str.rfind(str2) >= 0:
            type = '02'
    for str2 in list3:
        if str.rfind(str2) >= 0:
            type = '03'
    for str2 in list4:
        if str.rfind(str2) >= 0:
            type = '04'
    for str2 in list5:
        if str.rfind(str2) >= 0:
            type = '05'
    for str2 in list6:
        if str.rfind(str2) >= 0:
            type = '06'
    if type is None:
        type = '07'
    return type


def get_type():
    conn = pymysql.connect(#host='localhost',
                           host='192.168.11.251',
                           port=3306,
                           user='root',
                           password='youtong123',
                           # password='mysql',
                           database='sipai',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)  # 默认返回元祖，加上这个参数返回的是字典结构


    with conn.cursor() as cur1:
        # sql1 = "SELECT id,title from land_sum_info a WHERE a.confidence is not Null;"
        # sql1 = "SELECT id,asset_name,asset_type from sm_auction a WHERE a.asset_type is NULL;"
        sql1 = "SELECT id,title,house_type from increment_data_copy a WHERE a.house_type is NULL;"
        cur1.execute(sql1)
        #设定游标从第一个开始移动
        cur1.scroll(0, mode='absolute')
        #获取此字段的所有信息
        results = cur1.fetchall()
        # print(results)
        for result in results:
            #获取字典中的字段信息
            id = result["id"]
            title = result["title"]
            house_type = modify_type(title)

            #将bid_id字段信息更新成唯一的uuid信息即titlt_id
            with conn.cursor() as cur2:
                # sql2 = "update sm_auction set asset_type = %s where id = %s "
                sql2 = "update increment_data_copy set house_type = %s where id = %s "
                cur2.execute(sql2, (house_type,id))
                print(id,house_type)
                conn.commit()
                conn.cursor().close()
                print("**" * 50)


if __name__ == '__main__':
    get_type()
