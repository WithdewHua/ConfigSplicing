#!/usr/bin/python
# -*-coding:utf-8 -*-
#
# Copyright:WithdewHua
# modified: 2019-08-07


from functions import choose_nodes, write_config
from nodes import GetNodes
from rules import GetRules


def main():
    """项目主程序"""
    # 处理托管链接和规则链接
    node_urls = input('请输入 Surge/SS 订阅链接（多个链接用空格间隔）：').strip()
    print('节点获取中...')
    # 获取节点和节点名字
    [nodes, node_names] = GetNodes(node_urls).get_ss()
    rule_url = input('请输入规则链接（默认神机规则）：').strip()
    if rule_url == '':
        rule_url = 'https://raw.githubusercontent.com/ConnersHua/Profiles/master/Surge/Pro.conf'
    else:
        rule_url = rule_url
    print('规则获取中...')
    # 获取 Surge 格式规则
    [general, group_names, rule] = GetRules(rule_url).surge()
    # 询问各个策略组的节点选择
    chosen_dict = choose_nodes(node_names, group_names)
    # 拼接出新的 Proxy Group 列表
    proxy_group = ['\n[Proxy Group]\n']
    for key, value in chosen_dict.items():
        proxy_group.append(key + ' = ' + ', '.join(value) + '\n')
    proxy_group.append('\n')
    # 生成新的配置
    new_config = general + nodes + proxy_group + rule

    # 写入文件
    new_config = write_config(new_config, group_names)
    # 结束提示
    print('脚本运行结束,请在 results 文件夹查看文件!')


main()
