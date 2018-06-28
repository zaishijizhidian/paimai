# -*- coding: utf-8 -*-
import re

from lxml import etree

import requests

# detail_url = "https://desc.alicdn.com/i4/550/370/556377224062/TB1KOKGSFXXXXa3XXXX8qtpFXlX.desc%7Cvar%5Edesc%3Bsign%5E6cf45d90113d853cd2bf957b980ce925%3Blang%5Egbk%3Bt%5E1505441171"
# detail_url = "https://paimai.jd.com/json/paimaiProduct/productDesciption?productId=25776048918"
# detail_url = "https://desc.alicdn.com/i6/550/490/555496393444/TB1tGFNSpXXXXcdXVXX8qtpFXlX.desc%7Cvar%5Edesc%3Bsign%5E1306f46cca017b25c951430327c37f5c%3Blang%5Egbk%3Bt%5E1500256668"
detail_url = "https://desc.alicdn.com/i1/551/330/558330564182/TB1xB7Hfh3IL1JjSZPf8qwrUVla.desc%7Cvar%5Edesc%3Bsign%5E402f6f2e73d52069efc8d48595107c80%3Blang%5Egbk%3Bt%5E1507860086"
# detail_url = 'https://desc.alicdn.com/i7/520/880/526880947623/TB1uNsRLpXXXXaQXVXX8qtpFXlX.desc%7Cvar%5Edesc%3Bsign%5E8e1ab3c370d8cdeb63eb777dcb92f4f4%3Blang%5Egbk%3Bt%5E1453969092'
res = requests.get(detail_url)
res = etree.HTML(res.text)

# item = response.meta['item']
detail_desc =res.xpath("//*//text()")
# if not detail_desc:
#
#     detail_desc =  res.xpath("//table//text()")
# else:
#     detail_desc =  res.xpath("//span/text()")

print(detail_desc)
print("=====" * 20)
item = {}
if detail_desc is not None:
    detail_desc_temp = ','.join(detail_desc).strip()
    item["detail_desc"] = re.sub('\s', '', detail_desc_temp).replace(',', '')
else:
    item["detail_desc"] = None

print(item["detail_desc"])



str = "vardesc='该房屋坐落于高层（18层）住宅楼的底层，正房，钢混结构，2011年建成。"
print(len(str))