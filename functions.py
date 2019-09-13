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
        node_name = urllib.parse.unquote(node_name_str)
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
        node_name = urllib.parse.unquote(uri[(uri.find('#')) + 1:])
        # 处理节点的各个参数
        ss_params_tmp = base64.b64decode(base64_encode_str).decode('utf-8').split(':')
        if len(ss_params_tmp) != 3:
            print('链接有误！请检查链接')
            return
        else:
            password_and_server = ss_params_tmp[1].split('@')
            ss_params = [password_and_server[1], ss_params_tmp[2], ss_params_tmp[0], password_and_server[0]]
    return [node_name, ss_params]


def choose_nodes(node_names, group_names):
    """
    为策略组选择节点和策略方式
    :param node_names: 获取到的节点名字
    :param group_names: 规则中的策略组名字
    :return:
    """

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
        while True:
            string = input('请为 ' + group_names[k] + ' 挑选（输入数字,0-2必选一个，输入666全选所有节点）：')
            num_list = string.strip().split(" ")
            tmp_list = []
            try:
                for v in num_list:
                    v = int(v)
            except ValueError:
                print('请输入正确的数字')
                continue
            else:
                # 666 时添加所有节点
                if v == 666:
                    for g in range(len(node_names)):
                        m = g + len(group_names) + 5
                        tmp_list.append(node_dict[m])
                else:
                    tmp_list.append(node_dict[v])
                break
        chosen_dict[group_names[k]] = tmp_list
    return chosen_dict


def change_group_name(group_names):
    """
    修改策略组名字
    :param group_names: 原策略组名字
    :return: 新旧策略组名字字典
    """

    group_name_changed_dict = {}
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
                continue

    return group_name_changed_dict
