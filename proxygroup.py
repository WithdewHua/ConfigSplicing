# -*- coding:utf-8 -*-
# Copyright: WithdewHua
# 2019-09-14
#

from functions import input_new_group_name


class ProxyGroup:
    """
    策略组处理
    """

    def __init__(self, nodes_name, groups_name, interval):
        """
        初始化
        :param nodes_name: 节点名列表
        :param groups_name: 策略组名列表
        :return:
        """

        self.nodes_list = nodes_name
        self.groups_name = groups_name
        # 策略类型列表
        self.type_list = ['select', 'url-test', 'fallback', 'load-balance']
        # 可用参数列表
        self.params_dict = dict(url='http://www.gstatic.com/generate_204', interval=interval)
        self.chosen_dict = dict(name='', type='', proxies=[])
        self.chosen_list = []

    def choose_type(self, group_name):
        """
        选择策略组的策略方式
        :param group_name: 策略名
        :return:
        """
        # 展示所有可供选择的内容
        print('可供策略组 ' + group_name + ' 选择的策略方式有：')
        for i, el in enumerate(self.type_list):
            print(i, el)
        while True:
            # 检查输入是否为数字
            try:
                num = int(input('请输入您的选择：'))
            except ValueError:
                print('请输入数字！')
                continue
            else:
                # 检查输入是否超过序号值
                try:
                    self.chosen_dict.update(dict(name=group_name, type=self.type_list[num]))
                except IndexError:
                    print('请输入正确的序号！')
                    continue
                else:
                    break

    def choose_policy(self, group_name):
        """
        选择可用的策略组
        :param group_name: 策略组名字
        :return:
        """

        avail_group = list(self.groups_name)
        avail_group.remove(group_name)
        avail_group.extend(['DIRECT', 'REJECT'])
        # 展示该策略可用的策略名
        print('可供策略组 ' + group_name + ' 引用的策略组有：')
        for i, el in enumerate(avail_group):
            print(i, el)
        while True:
            # 检查输入是否为数字
            try:
                str_list = input('请输入您的选择(回车跳过)：').split()
                for num in str_list:
                    num = int(num)
                    try:
                        self.chosen_dict['proxies'].append(avail_group[num])
                    except IndexError:
                        print('请输入正确的序号！')
                        continue
                    else:
                        continue

            except ValueError:
                print('请输入数字！')
                continue
            else:
                break

    def choose_node(self, group_name):
        """
        选择策略组的
        :param group_name:
        :return:
        """

        # 展示所有可选的节点
        print('可供策略组 ' + group_name + ' 选择的节点有：')
        for i, el in enumerate(self.nodes_list):
            print(i, el)
        while True:
            # 检查输入是否为数字
            try:
                str_list = input('请输入您的选择(回车不选，666 全选)：').split()
                # 如果为空代表不选
                if not str_list:
                    break
                # 666 全选
                if len(str_list) == 1 and int(str_list[0]) == 666:
                    self.chosen_dict['proxies'].extend(self.nodes_list)
                # 其他值则选定了具体的节点
                else:
                    for num in str_list:
                        num = int(num)
                        try:
                            self.chosen_dict['proxies'].append(self.nodes_list[num])
                        except IndexError:
                            print('请输入正确的序号！')
                            break
                        else:
                            continue

            except ValueError:
                print('请输入数字！')
                continue
            else:
                break

    def add_params(self):
        """
        选择一些可用参数
        :return:
        """

        if self.chosen_dict['type'] in ['url-test', 'fallback', 'load-balance']:
            self.chosen_dict.update(self.params_dict)


def get_proxy_group(nodes_name, groups_name, interval, rename):
    """
    构造出新的 proxy group
    :return: 构造好的 proxy group 列表
    """

    pg = ProxyGroup(nodes_name, groups_name, interval)

    if rename:
        pg.groups_name, changed_group_dict = input_new_group_name(groups_name)
    else:
        changed_group_dict = {}

    for group_name in pg.groups_name:
        pg.chosen_dict = dict(name='', type='', proxies=[])
        pg.choose_type(group_name)
        pg.choose_policy(group_name)
        pg.choose_node(group_name)
        pg.add_params()
        pg.chosen_list.append(pg.chosen_dict)

    return pg.chosen_list, changed_group_dict
