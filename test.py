#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/5 15:51
# @Author  : haifengzuishuai
# @Email   : dada0614@126.cm
# @File    : test.py
import hashlib

a = '8.mp4'
print(a.split('.')[1])
h1=hashlib.md5()
# 在h1 上面更新所需要加密的字符串
h1.update(str.encode(encoding='utf-8'))
# 获取加密后的字符串
print(h1.hexdigest())
