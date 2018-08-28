# -*- coding: utf-8 -*-
import requests

from PAIMAI.middlewares import ProxyMiddleware


def get_html():
    PROXY_URL = 'http://localhost:5555/random'
    proxy = ProxyMiddleware(PROXY_URL)
    pr = proxy.get_random_proxy()
    print(pr)
    # proxy_url = 'https://{proxy}'.format(proxy=pr)
    proxies = {
        'http': 'http://' + pr
    }
    headers = {
    # 'authority': 'sf.taobao.com',
    # 'method': 'GET',
    # 'path': '/ item_list.htm?spm = a213w.3064813.a214dqe.1.s5mfNi',
    # 'scheme': 'https',
    'accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
    'accept - encoding': 'gzip, deflate, br',
    'accept - language': 'zh - CN, zh;q = 0.9, en;q = 0.8, en - US;q = 0.7',
    'referer':'https://sf.taobao.com/?spm=a213w.3065169.sfhead2014.2.UZZ6aa&current=index',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    start_url = 'https://sf.taobao.com/item_list.htm?spm=a213w.7398504.filter.2.EClmw1&category=50025969&auction_start_seg=-1'
    # res  = requests.get('https://sf.taobao.com/item_list.htm',)
    response = requests.get(start_url, allow_redirects=False, proxies=proxies, timeout=5)
    print(response.status_code)
    try:
        if response.status_code == 302:
            get_html()
    except Exception:
        print("false")
    else:
        print(response.text)


if __name__ == '__main__':
    get_html()