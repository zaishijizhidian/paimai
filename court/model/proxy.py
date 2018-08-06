# -*- coding: utf-8 -*-
from lxml import etree

import requests
table_name = 'sm_court'
import pymysql
main_fields = ['court', 'address', 'phone_num']

from user_agent import header
headers = header()

# headers = { #'Cookie':'userSelectCity=hangzhou; areaInfo=0XfPn5QEJpsyUE%2B94tMxwdUbO4UgveLGKkpfz%2F460mglmsSxiXOd6CH6GKSza7vjjVElZ2Wyu57TyPMKqdP8xrCDgX4CWZBySRk4bX4; uuid=DhF5WFsfabgXKCH8CKiPAg==; product_areaInfo=13jInsMCdM4yUFarr59qnYZPVNR%2B%2BvPMK1dTg%2BYywjB0xJPnw3%2BBvnSHCaS5fLHiilElZ3VmPjYFSUAK5p7qwbCI2htBzWi%2Bz8HCKiEIHG2P; PHPSESSID=sjo0ag20vlbtdfere84kblj422; Hm_lvt_ab3790496cb8e9723320f258938d16d3=1528785337,1530607714,1530668885,1530758126; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; Hm_lpvt_ab3790496cb8e9723320f258938d16d3=1530771163',
#             'Host': 'www.lawtime.cn',
#             'Referer': 'http://www.lawtime.cn/fayuan/city/tianjin',
#             'Upgrade-Insecure-Requests':'1',
#             'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
#             }


proxy_pool_url = 'http://localhost:5000/get'
proxy = None #全局参数：IP


max_count = 8
# item = {}
pro_list = []
city_list = []
item = {}
# 获取代理IP
def get_proxy(pool):
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_html(url, count=1):
    print('正在请求', url)
    print('尝试次数', count)
    global proxy
    if count >= max_count:
        print('请求次数太多')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }

            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies, timeout=5)
            print("有代理")
            print(response.status_code)


        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        # print('HTTP代码', response.status_code)
        if response.status_code == 200:
            res = response.text
            print(res)
            html = deal_html(res)
            return html
        if response.status_code == 302 or response.status_code == 304:
            print('302')
            proxy = get_proxy(proxy_pool_url)
            print(proxy)
            if proxy:
                print('获得代理ip：', proxy)
                return get_html(url, count)
            else:
                print('Get Proxy Failed')
                return None
        if response.status_code == 404 or response.status_code == 429:
            print('404')
            proxy = get_proxy(proxy_pool_url)
            print(proxy)
            if proxy:
                print('获得代理ip：', proxy)
                return get_html(url, count)
        if response.status_code == 301:
            print('301')
            proxy = get_proxy(proxy_pool_url)
            print(proxy)
            if proxy:
                print('获得代理ip：', proxy)
                return get_html(url, count)
            else:
                print('Get Proxy Failed')
                return None
        return None
    except ConnectionError as e:
        proxy = get_proxy(proxy_pool_url)
        count += 1
        print('Error Occurred', e.args)
        return get_html(url, count)
    except requests.exceptions.Timeout:
        proxy = get_proxy(proxy_pool_url)
        count += 1
        print('请求超时：', requests.exceptions.Timeout.args)
        return get_html(url, count)
    except TypeError:
        proxy = get_proxy(proxy_pool_url)
        count += 1
        print('请求失败!尝试重新请求....')
        return get_html(url, count)
    except requests.exceptions.ConnectionError as e:
        print(e)
        proxy = get_proxy(proxy_pool_url)
        count += 1
        print('请求失败!尝试重新请求....')
        return get_html(url, count)


def deal_html(text):
    html_text = etree.HTML(text)
    return html_text


def get_province(url):
    html = get_html(url)
    # 获取所有省的的url链接
    if html is not None:
        provice_list = html.xpath("//div[@class='warp2']//div[@class='trends']//p//a/@href")
        # print(provice_list)

        if provice_list:
            for provice in provice_list[4:]:
                province_url = provice.strip()
                pro_list.append(province_url)

        return pro_list


def get_city1_url(url):
    city_list1 = []
    html = get_html(url)
    if html is not None:
    # 获取所有省的的url链接
        provice_list = html.xpath("//div[@class='warp2']//div[@class='trends']//p//a/@href")
        # print(provice_list)

        if provice_list:
            for city in provice_list[:4]:
                city_url = city.strip()
                city_list1.append(city_url)

        return city_list1

def get_city2_url(url):
    city_list2 = []
    html = get_html(url)
    if html is not None:
        city_list = html.xpath("//div[@class='midarea ma2']//div[@class='mcol']//span[@class='right']//a/@href")
        # 遍历所有市,找出所有县的url
        for city in city_list:
           city_url = city.strip()
           city_list2.append(city_url)

        return city_list2

def get_court_url(html):
    item = {"court":'',"phone_num":'',"address":''}
    # html = get_html(url)
    if html is not None:

    # item = response.meta["item"]
    #法院信息列表

        court_list = html.xpath("//div[@class='midarea ma2']//div[@class='mcol']//dl")


        if court_list:
            for court in court_list:
                # print(court)
                court_temp = court.xpath(".//dt[@class='mccname']//text()")
                item["court"] = court_temp[0] if court_temp else ''
                # print(item["court"])

                phone_num_temp = court.xpath(".//dd[2]//text()")
                item["phone_num"] = phone_num_temp[0] if phone_num_temp else ''
                # print(item["phone_num"])

                address_temp = court.xpath(".//dd[3]//text()")
                item["address"] = address_temp[0] if address_temp else ''
                # print(item["address"])
                print(item)
                save_content(item)
                print("****"*10)
                    # return item

    #下一页

        next_url_temp = html.xpath("//a[contains(.,'下一页')]/@href")
        next_url = next_url_temp[0] if next_url_temp else None
        if next_url is not None:
            htm = change(next_url)
            get_court_url(htm)
    # print(item)
    return item


def save_content(item):
    conn = pymysql.connect(host='192.168.11.251',
                                port=3306,
                                user='root',
                                password='youtong123',
                                database='sipai',
                                charset='utf8')
    cur = conn.cursor()
    sql = 'INSERT INTO {0}({1}) VALUES({2})'.format(table_name, ','.join(main_fields),','.join(['%s'] * len(main_fields)))
    args = [item[k] for k in main_fields]
    arg = tuple(args)
    cur.execute(sql, arg)
    conn.commit()
    print("提交成功")
    cur.close()
    conn.close()
    # print(item)
    # return item



def run():
    global item
    url = 'http://www.lawtime.cn/fayuan/'
    pro_url = get_province(url)
    print(pro_url)
    city_list1 = get_city1_url(url)
    print(city_list1)
    # for city in city_list1:
    #     get_court_url(city)
        # print(item)
        # try:
        #     save_content(item)
        # except Exception as e:
        #     print(e)
        #     pass
    # print(city_list1)
    # for pro in pro_url:
    #     city_list2 = get_city2_url(pro)
    #     for city in city_list2:
    #         get_court_url(city)
            # print(item)
            # try:
            #     save_content(item)
            # except Exception as e:
            #     print(e)
            #     pass
def change(url):

    response = requests.get(url, headers=headers)
    print('HTTP代码', response.status_code)
    if response.status_code == 200:
        res = response.text
        # print(res)
        # html = deal_html(res)
        html = etree.HTML(res)
        return  html

if __name__ == '__main__':
    list = ['http://www.lawtime.cn/fayuan/province/beijing']
    for url in list:
        html = change(url)


        get_court_url(html)
    # for pro in list:
    #     city_list2 = get_city2_url(pro)
    #     for city in city_list2:
    #         get_court_url(city)
    # run()
