#!/usr/bin/python
# -*- coding:utf-8 -*-
# Copyright: WithdewHua
# 2019-08-05

import re
import os
import wget
from config import read_config
from ruamel import yaml


class GetRules:
    """
    获取规则
    """

    def __init__(self, url):
        """
        初始化
        :param url: 规则链接
        """

        self.url = url
        # 获取整个文件内容并存入字符串数组中
        self.config = read_config(self.url)
        self.surge_rules = []
        self.clash_rules = {}

    def surge(self):
        """获取 Surge 格式的规则"""

        # 存到规则列表中
        for rule in self.config:
            rule = rule.decode('utf-8')
            self.surge_rules.append(rule)

        # 获取各个关键字段的数组索引值
        for rule in self.surge_rules:
            if re.search(r'\[General\]', rule):
                general_start = self.surge_rules.index(rule)
            if re.search(r'\[Proxy\]', rule):
                proxy_start = self.surge_rules.index(rule)
            if re.search(r'\[Proxy Group\]', rule):
                group_start = self.surge_rules.index(rule)
            if re.search(r'\[Rule\]', rule):
                rule_start = self.surge_rules.index(rule)

        # 生成各部分字段数组
        general = self.surge_rules[general_start:proxy_start]
        group = self.surge_rules[group_start:rule_start]
        rule = self.surge_rules[rule_start:]

        # 获取策略组名字和策略
        group_names = []
        for li in group:
            res = re.search(r'(.+)=\s+(select|url-test|fallback)', li)
            res2 = re.search(r'(#.+)', li)
            # 只获取非注释的策略组
            if (res is not None) and (res2 is None):
                group_names.append(res.group(1).strip())
        return general, group_names, rule

    def clash(self):
        """
        获取 Clash 格式的规则
        :return:
        """

        # 下载规则文件
        out_file = 'config.yaml'
        wget.download(self.url, out=out_file)
        # 读取规则文件
        with open(out_file, 'r', encoding='utf-8') as f:
            self.clash_rules = yaml.load(f, Loader=yaml.RoundTripLoader)
        # 读取对象后删除下载文件
        os.remove(out_file)
        return self.clash_rules
