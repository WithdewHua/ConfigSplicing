# -*- coding:utf-8 -*-
# Copyright: WithdewHua
# 2019-08-08

import base64
import urllib.parse


def parse_ss(uri):
    """
    解析 ss URI
    :param uri: ss uri 链接
    :return:
    """

    # 格式一：只 base64 编码加密和密码
    if '@' in uri:
        base64_encode_str = uri[5:uri.find('@')]
        # 判断是否需要补充字符
        missing = len(base64_encode_str) % 4
        if missing != 0:
            base64_encode_str += '=' * (4 - missing)
        server_and_port = uri[(uri.find('@') + 1):uri.find('#')]
        node_name_str = uri[(uri.find('#') + 1):]

        # 将节点名字用 unquotes 解码出来
        node_name = urllib.parse.unquote(node_name_str).strip()
        # base64 解码
        method_and_password = base64.b64decode(base64_encode_str).decode('utf-8')

        # 将 method password server port 放入一个列表中
        list1 = method_and_password.split(':')
        list2 = server_and_port.split(':')
        ss_params = list2 + list1

    # 格式二：将加密、密码、服务器、端口全部进行 base64 编码
    else:
        base64_encode_str = uri[5:uri.find('#')]
        # 判断是否需要补充字符
        missing = len(base64_encode_str) % 4
        if missing != 0:
            base64_encode_str += '=' * (4 - missing)

        # 解码，以 # 为分界点，后面的即为节点名字
        node_name = urllib.parse.unquote(uri[(uri.find('#')) + 1:]).strip()
        # 处理节点的各个参数
        ss_params_tmp = base64.b64decode(base64_encode_str).decode('utf-8').split(':')
        if len(ss_params_tmp) != 3:
            print('链接有误！请检查链接')
            return
        else:
            password_and_server = ss_params_tmp[1].split('@')
            ss_params = [password_and_server[1], ss_params_tmp[2], ss_params_tmp[0], password_and_server[0]]
    return node_name, ss_params


def input_new_group_name(group_names):
    """
    修改策略组名字
    :param group_names: 原策略组名字
    :return: 新旧策略组名字字典
    """

    group_name_changed_dict = {}
    new_group_name = list(group_names)
    print('原策略组名字分别为：')
    for i, el in enumerate(group_names):
        print(i, el)
    while True:
        str1 = input('请选择需要更名的策略组（回车退出）：').strip()
        if str1 == '':
            break
        else:
            try:
                index = int(str1)
            except ValueError:
                print('请输入正确的序号')
                continue
            else:
                if index > len(group_names) - 1:
                    print('序号输入错误！不能超过策略组个数！')
                else:
                    str2 = input('请输入新名字：').strip()
                    group_name_changed_dict[group_names[index]] = str2
                    new_group_name[index] = str2
                continue

    return new_group_name, group_name_changed_dict


def get_group_name_from_clash(clash_yaml):
    """
    获取 clash 策略组名
    :param clash_yaml: clash 规则文件
    :return: 策略组名列表
    """

    proxy_group = clash_yaml['Proxy Group']
    group_names = []
    for group in proxy_group:
        name = group['name']
        group_names.append(name)
    return group_names


def change_rule_policy(changed_group_dict, rule_list):
    """
    为配置中的规则更改策略组名字
    :param changed_group_dict: 新旧策略名列表
    :param rule_list: 配置文件中的规则字段列表
    :return: 更改策略名后的规则字段列表
    """

    new_rules = []
    for rule in rule_list:
        for key, value in changed_group_dict.items():
            rule = rule.replace(key, value)
        new_rules.append(rule)
    return new_rules
