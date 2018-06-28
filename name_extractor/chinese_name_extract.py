# -*- coding: utf-8 -*-

# 中文人名识别算法

import jieba, re, codecs, json, os
from functools import reduce
from collections import Counter
import math, time

class ChineseNameTool:
    
    def __init__(self, family_name_file, full_name_file, dict_file=None, threshold=18):
        self.threshold = threshold
        self.path = os.popen("pwd").read().strip()
        # self.path = os.popen("pwd").read().strip()+'/tools_t/' #linux中的相对路径
        with codecs.open(self.path +"/" +family_name_file, 'r', 'utf-8') as f:
            L = reduce(lambda x,y:x+y, \
                      [line.strip().split('\t') for line in f.readlines()])
            self.family_names = set(list(L))
        with codecs.open(self.path +"/" +full_name_file, 'r', 'utf-8') as f:
            self.full_names = [line.strip() for line in f.readlines()]
            self.self_names = [name[2:] if name[:2] in self.family_names else name[1:] for name in self.full_names]
            self.self_name_chars = ''.join(self.self_names)
            L = float(len(self.self_name_chars))
            self.self_name_chars = Counter(self.self_name_chars)   #统计每个字的频率
            for key in self.self_name_chars:
                self.self_name_chars[key] /= L
        
        self.full_names = set(self.full_names)
        self.self_names = set(self.self_names)
        
        if dict_file:
            with codecs.open(self.path + dict_file, 'r', 'utf-8') as f:
                self.dict_list = set([line.strip() for line in f.readlines()])
    
    def predict_prob(self, s):
        if s in self.full_names:
            return 0
        if len(s) <= 1 or len(s) >= 10:
            return 1000000
        if s[:2] in self.family_names and s[2:]:
            _name_ = s[2:]
        elif s[0] in self.family_names:
            _name_ = s[1:]
        else:
            return 1000000
        
        try:
            ng_log_prob = sum(list(map(lambda x:-math.log(self.self_name_chars[x]), list(_name_))))
        except:
            if u'某' in _name_ or u'×' in _name_:
                return 0
            ng_log_prob = 1000000
        
        return ng_log_prob
        
    def is_name(self, s):
        return self.predict_prob(s) <= self.threshold
        
    def max_name(self, start_part, str_list, max_len_get):
        ss, j = '', 0
        while len(ss) <= max_len_get:
            try:
                next_ = str_list[j]
            except:
                return ss
            ss += next_
            if self.is_name(start_part+ss):
                j += 1
            else:
                ss = ss[:len(ss)-len(next_)]
                return ss
    
    def extractChineseName(self, text):
        text_list = list(jieba.cut(text, cut_all=False))
        name_list = []
        for i, s in enumerate(text_list):
            if len(s) == 1:
                if s in self.family_names:
                    ss = self.max_name(s, text_list[i+1 :], 3)
                    if ss:
                        name_list.append(s + ss)
            elif len(s) == 2:
                if s in self.family_names:
                    ss = self.max_name(s, text_list[i+1 :], 3)
                    if ss:
                        name_list.append(s + ss)
                elif s[0] in self.family_names and self.is_name(s):
                    ss = self.max_name(s, text_list[i+1 :], 2)
                    name_list.append(s + ss)
            elif len(s) == 3:
                if self.is_name(s):
                    name_list.append(s)
        return list(set(name_list))
        
if __name__ == '__main__':
    
    m = ChineseNameTool('family_names.txt', 'chinese_names.txt')
    #print(m.is_name(u'原告靳瀚办理位于昌吉市2区7丘12栋1-1商业房屋'))
    # s = u"被告马艳于判决生效后七日内协助原告靳瀚办理位于昌吉市2区7丘12栋1-1商业房屋的国有土地使用证过户手续，相关过户费用由原告靳瀚承担；本案受理费35元，其他诉讼费用80元，合计115元，由原告靳瀚和被告马艳各负担57.50元（本案受理费及其他诉讼费用已由原告预交，所预交的费用在本案执行时按判决书确定的数额由被告一并向原告支付）。如不服本判决，可在判决书送达之日起十五日内，向本院递交上诉状，并按对方当事人的人数提出副本，上诉于昌吉回族自治州中级人民法院。本判决发生法律效力后，当事人必须履行，一方当事人拒绝履行的，对方当事人可以向本院申请执行，申请执行的期限为二年，若超过法定期限提出申请执行的，本院则依法不予受理"
    # s = u"被告马艳于判决生效后七日内协助原告靳瀚办理位于昌吉市2区7丘12栋1-1商业房屋的国有土地使用证过户手续"
    s = '吴江市金鑫农村小额贷款有限公司李晓云钟春荣'
    print(m.extractChineseName(s))
    #print(json.dumps(m.extractChineseName(s), ensure_ascii=False).encode('utf-8'))
