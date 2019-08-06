#!/usr/bin/python
# -*- coding:utf-8 -*-
# Copyright: WithdewHua
# 2019-08-05

import re
import func


class GetRules(object):
    def __init__(self, url):
        # 获取整个文件内容并存入字符串数组中
        self.config = func.get_page(url).readlines()
        self.rules = []
        for rule in self.config:
            rule = rule.decode('utf-8')
            self.rules.append(rule)

    def surge(self):
        # 获取各个关键字段的数组索引值
        for rule in self.rules:
            if re.search(r'\[General\]', rule):
                general_start = self.rules.index(rule)
            if re.search(r'\[Proxy\]', rule):
                proxy_start = self.rules.index(rule)
            if re.search(r'\[Proxy Group\]', rule):
                group_start = self.rules.index(rule)
            if re.search(r'\[Rule\]', rule):
                rule_start = self.rules.index(rule)
        # 生成各部分字段数组
        general = self.rules[general_start:proxy_start]
        group = self.rules[group_start:rule_start]
        rule = self.rules[rule_start:]
        # 获取策略组名字和策略
        group_names = []
        for li in group:
            res = re.search(r'(.+)=\s+(select|url-test|fallback)', li)
            res2 = re.search(r'(#.+)', li)
            if (res is not None) and (res2 is None):
                group_names.append(res.group(1))
        return [general, group_names, rule]
