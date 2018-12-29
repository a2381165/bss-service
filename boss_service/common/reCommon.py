#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 0019 16:20
# @Site    : 
# @File    : reCommon.py
# @Software: PyCharm

import re

# 正则匹配电话号码
def rePhone(phone):
    p2 = re.compile('^1[358]\d{9}$|^147\d{8}')
    phonematch = p2.match(phone)

    if phonematch:
        if phonematch.group():
            return True
        else:
            return False
    else:
        return False

# 正则匹配邮箱和电话号码
def reEmail(email):
    c = re.compile(r'^\w+@(\w+\.)+(com|cn|net|edu)$')
    s = c.search(email)
    if s:
        if s.group():
            return True
        else:
            return False
    else:
        return False



