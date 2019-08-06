# -*- coding:utf-8 -*-
# Copyright: WithdewHua
# 2019-08-05

import re
import base64
import func


def choose_nodes(node_names, group_names):
    """为策略组选择节点和策略方式"""
    # 将所有可选项放进一个字典中，包括节点、策略组以及策略方式,显示顺序为策略方式 -> 策略组名 -> 节点
    node_dict = {0: 'select', 1: 'url-test', 2: 'fallback', 3: 'DIRECT', 4: 'REJECT'}
    for h in range(len(group_names)):
        node_dict[5 + h] = group_names[h]
    for i in range(len(node_names)):
        node_dict[len(group_names) + 5 + i] = node_names[i]
    # 可选参数
    params = ['url=http://www.gstatic.com/generate_204']
    for i in range(len(params)):
        node_dict[len(group_names) + len(node_names) + 5 + i] = params[i]
    # 为策略组选择节点
    chosen_dict = {}
    for k in range(len(group_names)):
        print('策略 ' + group_names[k] + ' 可供选择的内容有： ')
        for key, value in node_dict.items():
            print(str(key) + ": " + value)
        string = input('请为 ' + group_names[k] + ' 挑选（输入数字,0-2必选一个，输入666全选所有节点）：')
        num_list = string.strip().split(" ")
        tmp_list = []
        for v in num_list:
            v = int(v)
            if v == 666:
                for g in range(len(node_names)):
                    m = g + len(group_names) + 5
                    tmp_list.append(node_dict[m])
            else:
                tmp_list.append(node_dict[v])
        chosen_dict[group_names[k]] = tmp_list
    return chosen_dict


class Nodes(object):
    def __init__(self, url):
        # 获取整个文件内容并存入字符串数组中
        self.config = func.get_page(url).readlines()
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
        nodes_str = base64.b64decode(self.config[0]).decode('utf-8').strip()
        nodes_list = nodes_str.split('\n')
        nodes_dict = {}
        for node in nodes_list:
            [node_name, ss_params] = func.parse_ss(node)
            nodes_dict[node_name] = ss_params
        for key, value in nodes_dict.items():
            join = key + ' = custom' + ', ' + ', '.join(value) + ', udp-relay=true' + '\n'
            self.nodes.append(join)
            self.node_names.append(key)
        return [self.nodes, self.node_names]
