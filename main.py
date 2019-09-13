#!/usr/bin/python
# -*-coding:utf-8 -*-
#
# Copyright:WithdewHua
# modified: 2019-08-07

import click

from functions import choose_nodes
from config import write_config
from getnodes import GetNodes
from getrules import GetRules


@click.command()
@click.option('-r', '--rule_url', default='https://raw.githubusercontent.com/ConnersHua/Profiles/master/Surge/Pro.conf',
              help='规则链接（默认为神机规则）')
@click.argument('sub_links', nargs=-1)
def main(sub_links, rule_url):
    """
    ConfigSplicing
    """

    try:
        # 处理托管链接和规则链接
        print('节点获取中...')
        # 获取节点和节点名字
        nodes, node_names = GetNodes(sub_links).get_ss()
        # 处理规则
        print('规则获取中...')
        # 获取 Surge 格式规则
        general, group_names, rules = GetRules(rule_url).surge()

        # 询问各个策略组的节点选择
        chosen_dict = choose_nodes(node_names, group_names)

        # 拼接出新的 Proxy Group 列表
        proxy_group = ['\n[Proxy Group]\n']
        for key, value in chosen_dict.items():
            proxy_group.append(key + ' = ' + ', '.join(value) + '\n')
        proxy_group.append('\n')

        # 生成新的配置
        new_config = general + nodes + proxy_group + rules

        # 写入文件
        write_config(new_config, group_names)

        # 结束提示
        print('脚本运行结束,请在 results 文件夹查看文件!')

    except (ImportError, EOFError, InterruptedError, KeyboardInterrupt) as e:
        print('\n' + '程序异常退出！ %s' % e)


if __name__ == '__main__':
    main()
