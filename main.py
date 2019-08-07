#!/usr/bin/python
# -*-coding:utf-8 -*-
#
# Copyright:WithdewHua
# modified: 2019-08-07

import os

import func.change_group_name
from nodes import choose_nodes, GetNodes
from rules import GetRules


def main():
    """项目主程序"""
    # 处理托管链接和规则链接
    _url = input('请输入序号（1. SS 订阅 2. Surge 托管）：')
    if int(_url) == 1:
        node_urls = input('请输入 SS 订阅链接（多个链接用空格间隔）：').strip()
        print('节点获取中...')
        [nodes, node_names] = GetNodes(node_urls).shadowsocks()
    if int(_url) == 2:
        node_url = input('请输入 Surge 托管链接（多个链接用空格间隔）：').strip()
        print('节点获取中...')
        [nodes, node_names] = GetNodes(node_urls).surge()
    rule_url = input('请输入规则链接（默认神机规则）：').strip()
    if rule_url == '':
        rule_url = 'https://raw.githubusercontent.com/ConnersHua/Profiles/master/Surge/Pro.conf'
    else:
        rule_url = rule_url
    print('规则获取中...')
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

    # 写入文件准备
    filename = input('为生成的文件取个好听的名字吧（默认 WithdewHua）：').replace(' ', '')
    if filename == '':
        filename = 'WithdewHua'
    path = os.path.dirname(__file__) + '/results/' + filename + '.conf'
    # 判断文件是否存在，若有则删除
    if os.path.exists(path):
        os.remove(path)
    # 询问是否需要更改策略组名称
    str1 = input('是否需要更改策略组名称（Y/n | 默认为否）').strip()
    if (str1 == 'Y') or (str1 == 'y'):
        group_name_dict = func.change_group_name.change_group_name(group_names)
        with open(path, mode='a+', encoding='utf-8') as f:
            for line in new_config:
                for key, value in group_name_dict.items():
                    line = line.replace(key, value)
                f.write(line)
    elif (str1 == 'N') or (str1 == 'n') or (str1 == ''):
        with open(path, mode='a+', encoding='utf-8') as f:
            for line in new_config:
                f.write(line)
    else:
        print('输入错误！')
        return
    print('脚本运行结束,请在 results 文件夹查看文件!')


main()
