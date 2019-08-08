# -*- coding:utf-8 -*-
# Copyright: WithdewHua
# 2019-08-08

import base64
import re

import functions as fun


class GetNodes(object):
    def __init__(self, urls):
        # 获取整个文件内容并存入字符串数组中
        self.config = fun.page(urls)
        # 初始化节点和节点名列表
        self.nodes = ['[Proxy]\n']
        self.node_names = []

    def surge(self):
        """输入链接为Surge托管"""
        for node in self.config:
            node = node.decode('utf-8')
            res = re.match(r'(.*)=\s*(custom|shadowsocks)', node)
            if res:
                self.nodes.append(node)
                self.node_names.append(res.group(1))
        self.nodes.append("\n")
        return [self.nodes, self.node_names]

    def shadowsocks(self):
        """输入链接为SS订阅"""
        _nodes = []
        nodes_list = []
        for i in range(len(self.config)):
            _nodes.append(base64.b64decode(self.config[i]).decode('utf-8').strip())
            nodes_list += _nodes[i].split('\n')
        nodes_dict = {}
        for node in nodes_list:
            [node_name, ss_params] = fun.parse_ss(node)
            nodes_dict[node_name] = ss_params
        for key, value in nodes_dict.items():
            join = key + ' = custom' + ', ' + ', '.join(value) + ', udp-relay=true' + '\n'
            self.nodes.append(join)
            self.node_names.append(key)
        return [self.nodes, self.node_names]
