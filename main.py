#!/usr/bin/python
# -*-coding:utf-8 -*-
#
# Copyright:WithdewHua
# modified: 2019-08-07

import click

from functions import get_group_name_from_clash, change_rule_policy
from config import write_surge_config, write_clash_config
from getnodes import GetNodes
from getrules import GetRules
from proxygroup import get_proxy_group


@click.command()
@click.option('-R', '--rename', is_flag=True, help='更改策略组名')
@click.option('-c', '--clash', is_flag=True, help='输出Clash配置文件')
@click.option('-r', '--rule', help='规则链接（默认为神机规则）')
@click.option('-i', '--interval', default=1200, help='设置延迟组的间隔时间（默认1200）')
@click.argument('sub_links', nargs=-1)
def main(sub_links, clash, rename, interval, rule=None):
    """
    ConfigSplicing
    """

    try:
        # Clash 配置文件
        if clash:
            # 采用默认规则链接
            if not rule:
                rule = 'https://raw.githubusercontent.com/ConnersHua/Profiles/master/Clash/Pro.yaml'
            # 处理托管链接和规则链接
            # 处理规则
            print('规则获取中...')
            # 获取 clash 格式规则
            clash_file = GetRules(rule).clash()
            print('节点获取中...')
            # 获取节点和节点名字
            nodes, node_names = GetNodes(sub_links).clash_nodes(clash_file)
            # 获取策略组名字
            group_names = get_group_name_from_clash(clash_file)
            # 询问各个策略组的节点选择
            groups, changed_group_dict = get_proxy_group(node_names, group_names, interval, rename)

            # 更名
            if rename:
                rules = change_rule_policy(changed_group_dict, clash_file['Rule'])
            else:
                rules = clash_file['Rule']

            # 写入文件
            write_clash_config(nodes, groups, rules, clash_file)

        # Surge 配置文件
        else:
            if not rule:
                rule = 'https://raw.githubusercontent.com/ConnersHua/Profiles/master/Surge/Pro.conf'
            # 处理托管链接和规则链接
            print('节点获取中...')
            # 获取节点和节点名字
            nodes, node_names = GetNodes(sub_links).surge_nodes()
            # 处理规则
            print('规则获取中...')
            # 获取 Surge 格式规则
            general, group_names, rules = GetRules(rule).surge()

            # 询问各个策略组的节点选择
            group_list, changed_group_dict = get_proxy_group(node_names, group_names, interval, rename)

            # 拼接出新的 Proxy Group 列表
            proxy_group = ['\n[Proxy Group]\n']
            for group_dict in group_list:
                group = group_dict['name'] + ' = ' + group_dict['type'] + ', ' + ', '.join(group_dict['proxies']) + '\n'
                proxy_group.append(group)
            proxy_group.append('\n')

            # 更名
            if rename:
                rules = change_rule_policy(changed_group_dict, rules)
            # 生成新的配置
            new_config = general + nodes + proxy_group + rules

            # 写入文件
            write_surge_config(new_config)

        # 结束提示
        print('脚本运行结束,请在 results 文件夹查看文件!')

    except (ImportError, EOFError, InterruptedError, KeyboardInterrupt) as e:
        print('\n' + '程序异常退出！ %s' % e)


if __name__ == '__main__':
    main()
