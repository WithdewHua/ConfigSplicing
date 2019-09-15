# -*- coding:utf-8 -*-
# Copyright: WithdewHua
# 2019-09-14
#

import os
from urllib import request

from ruamel import yaml


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


def write_surge_config(new_config):
    """
    将配置写入文件中
    :param new_config: 拼接后的配置文件
    :return:
    """

    # 写入文件准备
    filename = input('为生成的文件取个好听的名字吧（默认 WithdewHua）：').replace(' ', '')
    if filename == '':
        filename = 'WithdewHua'
    path = os.path.dirname(__file__) + '/results/' + filename + '.conf'

    with open(path, mode='w', encoding='utf-8') as f:
        for line in new_config:
            f.write(line)


def write_clash_config(proxy, proxy_group, rule, clash_yaml):
    """
    生成 clash 的配置文件
    :param rule: 规则列表
    :param proxy: 节点列表
    :param proxy_group: 策略组列表
    :param clash_yaml: 原规则文件
    :return:
    """

    clash_yaml.update({'Proxy': proxy, 'Proxy Group': proxy_group, 'Rule': rule})

    # 写入文件准备
    filename = input('为生成的文件取个好听的名字吧（默认 WithdewHua）：').replace(' ', '')
    if filename == '':
        filename = 'WithdewHua'
    path = os.path.dirname(__file__) + '/results/' + filename + '.yaml'

    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(clash_yaml, f, Dumper=yaml.RoundTripDumper, allow_unicode=True)
