# -*- coding:utf-8 -*-
# Copyright: WithdewHua
# 2019-09-14
#

from urllib import request
from functions import change_group_name
import os
import re


def read_config(urls):
    """
    读取节点或者规则链接
    :param urls: 节点链接或者规则链接
    :return: 读取的节点或者规则配置
    """

    # 修改 headers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/75.0.3770.142 Safari/537.36'}

    # 存放最后读取的配置文件
    pages = []

    # 判断链接为元组还是字符串
    if type(urls) == str:
        # 若为字符串（规则链接）
        page1 = request.Request(urls, headers=headers)
        page2 = request.urlopen(page1)
        pages = page2.readlines()

    if type(urls) == tuple:
        # 若为元组（节点链接）
        for url in urls:
            # 正常获取每个 URL 内容
            page1 = request.Request(url, headers=headers)
            page2 = request.urlopen(page1)
            # 将各个URL内容拼接在一个字符串数组中
            pages += page2.readlines()
    return pages


def write_config(new_config, group_names):
    """
    将配置写入文件中
    :param new_config: 拼接后的配置文件
    :param group_names: 策略组名字
    :return:
    """

    # 写入文件准备
    filename = input('为生成的文件取个好听的名字吧（默认 WithdewHua）：').replace(' ', '')
    if filename == '':
        filename = 'WithdewHua'
    path = os.path.dirname(__file__) + '/results/' + filename + '.conf'

    # 询问是否需要更改策略组名称
    while True:
        str1 = input('是否需要更改策略组名称（Y/[n]）').strip()
        if (str1 == 'Y') or (str1 == 'y'):
            # 改变策略组名字
            changed_group_name = change_group_name(group_names)
            with open(path, mode='w', encoding='utf-8') as f:
                for line in new_config:
                    for key, value in changed_group_name.items():
                        line = re.sub(key, value, line)
                    f.write(line)
            break
        elif (str1 == 'N') or (str1 == 'n') or (str1 == ''):
            # 不改变直接写入
            with open(path, mode='w', encoding='utf-8') as f:
                for line in new_config:
                    f.write(line)
            break
        else:
            print('输入错误！')
            continue
