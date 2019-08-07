# -*- coding:utf-8 -*-
# Copyright: WithdewHua
# 2019-08-05

import base64
import urllib.parse


def parse_ss(uri):
    """解析 ss URI"""
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
    else:
        base64_encode_str = uri[5:uri.find('#')]
        # 判断是否需要补充字符
        missing = len(base64_encode_str) % 4
        if missing != 0:
            base64_encode_str += '=' * (4 - missing)
        node_name = urllib.parse.unquote(uri[(uri.find('#')) + 1:])
        ss_params_tmp = base64.b64decode(base64_encode_str).decode('utf-8').split(':')
        if len(ss_params_tmp) != 3:
            print('链接有误！请检查链接')
            return
        else:
            password_and_server = ss_params_tmp[1].split('@')
            ss_params = [password_and_server[1], ss_params_tmp[2], ss_params_tmp[0], password_and_server[0]]
    return [node_name, ss_params]
