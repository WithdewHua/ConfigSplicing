# -*- coding:utf-8 -*-
# Copyright: WithdewHua
# 2019-08-05

from urllib import request


def page(urls):
    """修改 header"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/75.0.3770.142 Safari/537.36'}
    urls_li = urls.strip().split(' ')
    pages = []
    for url in urls_li:
        # 正常获取每个 URL 内容
        page1 = request.Request(url, headers=headers)
        page2 = request.urlopen(page1)
        # 将各个URL内容拼接在一个字符串数组中
        pages += page2.readlines()
    return pages
