# -*- coding:utf-8 -*-
# Copyright: WithdewHua
# 2019-08-09

import base64
import re

from config import read_config
import functions as fun


class GetNodes:
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
        self.nodes_dict = {}

    def get_ss(self):
        """
        从订阅链接或者托管链接获取节点
        :return: 节点字典
        """

        # 初始化
        _nodes = []
        _nodes_list = []

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
                _nodes_list += _nodes[-1].split('\n')

        # 处理字符串列表里面的 ss uri
        for node in _nodes_list:
            # 解析每个 ss uri
            # ss_params: [服务器、端口、加密方式、密码]
            node_name, ss_params = fun.parse_ss(node)
            # 存入节点字典中，key：节点名；value：节点参数
            self.nodes_dict[node_name] = ss_params

    def surge_nodes(self):
        """
        构造 Surge 格式的节点列表
        :return: Surge 格式的节点列表和节点名列表
        """

        self.get_ss()

        for key, value in self.nodes_dict.items():
            join = key + ' = custom' + ', ' + ', '.join(value) + ', udp-relay=true, tfo=true' + '\n'
            # 添加到节点列表
            self.nodes.append(join)
            self.node_names.append(key)
        return self.nodes, self.node_names

    def clash_nodes(self, clash_file):
        """
        构造 clash 格式的节点
        :return:
        """

        self.get_ss()

        # 初始化
        # clash 节点列表
        self.nodes = clash_file['Proxy']
        # 删除原文件中的示例节点
        self.nodes.clear()
        for key, value in self.nodes_dict.items():
            node = {}
            node.update(dict(name=key, type='ss', server=value[0], port=int(value[1]), cipher=value[2], password=value[3],
                             udp=True))
            self.nodes.append(node)
            self.node_names.append(key)
        return self.nodes, self.node_names

