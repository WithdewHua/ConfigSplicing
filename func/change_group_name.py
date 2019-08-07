# -*- coding:utf-8 -*-
# Copyright: WithdewHua
# 2019-08-05


def change_group_name(group_names):
    str1 = input('原策略组名字分别为：' + ' '.join(group_names) + '\n' + '请按照原策略组顺序依次填写新的策略名（空格分隔）：').strip()
    new_group_names = str1.split(" ")
    print(new_group_names)
    group_name_dict = {}
    for i in range(len(group_names)):
        group_name_dict[group_names[i]] = new_group_names[i]
    return group_name_dict
