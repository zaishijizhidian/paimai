# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
#求列表中数字的和
a = [('','1339.32'), ('', '471.17'), ('', '315.92')]
#
# #方法一,最原始的方法，先遍历列表，取出元祖里边的数字，但是也有局限性，只能在元祖中数字是空的情况，如果为非空，就无法采用了，那怎么解决这一类问题呢？看下面几种方法
# b = [''.join(i) for i in a]
#
# c = sum([float(m) for m in b])
#
# print(c)
# #方法二，采用python 内置模块map()函数和匿名函数lambda取出列表中元祖的第二行数据，转化成列表后求和
#
# n = sum(list(map(float,list(map(lambda x:x[1],a)))))
#
# print(n)

#方法三，采用pandas 和 numpy将列表转化为矩阵，然后求一列的数据之和
#使用pd.DataFrame()函数将列表装的元素转化为矩阵即二维数组
data = pd.DataFrame(a)
#将数组中的字符串类型转化为数据类型，并取第二列数据(下面３种写法都可以)
# df = pd.to_numeric(data[1])
# df = data[1].apply(pd.to_numeric)
df = data[1].astype(float)
#使用np中的sum函数求和
df1 = np.sum(df)
print(df1)

