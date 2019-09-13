# -*- coding:utf-8 -*-
# Copyright: WithdewHua
# 2019-08-09

import base64
import re

from config import read_config
import functions as fun


class GetNodes(object):
    """
    获取节点
    """

    def __init__(self, urls):
        """
        获取节点链接里的所有配置
        :param urls: 节点链接
        """

        # 获取整个文件内容并存入字符串数组中
        self.config = read_config(urls)
        # 初始化节点和节点名列表
        self.nodes = ['[Proxy]\n']
        self.node_names = []

    def get_ss(self):
        """
        从订阅链接或者托管链接获取节点
        :return: Surge 格式的节点列表以及其节点名
        """

        # 初始化
        _nodes = []
        nodes_list = []
        nodes_dict = {}

        # 遍历获取的节点配置，分离出 Surge 格式和 ss 格式
        for line in self.config:
            line = line.decode('utf-8').strip()
            # 匹配 Surge 格式节点
            res1 = re.search(r'(.*)=\s*(custom|shadowsocks)', line)
            # 匹配 ss base64 编码内容
            res2 = re.search(r'^[A-Za-z0-9+/]{8,}={0,2}$', line)
            if res1:
                # 对于 surge 格式来说直接添加即可
                self.nodes.append(line + '\n')
                self.node_names.append(res1.group(1))
            if res2:
                # 判断编码是否需要补充字符
                missing = len(line) % 4
                if missing != 0:
                    line += '=' * (4 - missing)
                # 将 base64 编码内容解码并转成字符串列表
                _nodes.append(base64.b64decode(line.encode()).decode().strip())
                nodes_list += _nodes[-1].split('\n')

        # 处理字符串列表里面的 ss uri
        for node in nodes_list:
            [node_name, ss_params] = fun.parse_ss(node)
            nodes_dict[node_name] = ss_params
        for key, value in nodes_dict.items():
            join = key + ' = custom' + ', ' + ', '.join(value) + ', udp-relay=true, tfo=true' + '\n'
            # 添加到节点列表
            self.nodes.append(join)
            self.node_names.append(key)
        return self.nodes, self.node_names
