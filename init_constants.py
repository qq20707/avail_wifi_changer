# coding:gbk
'''
Author:       无名Joker
Purpose:    初始化所有常量
Date:          2020年2月7日
Arguments:
Outputs:

json文件中
由上至下分别为：
最大重连次数
默认网卡序号
允许当前网络与次优网络的最大延迟差值(避免频繁切换带来的开销)
允许的最大延迟
允许的最大丢包率
不需切换时程序休眠的时间
默认PING的IP或URL


Dependencies:

History:
--------------------------------------------------------------
Date:
Author:
Modification:
--------------------------------------------------------------
'''


import json


def reload_json(file_name):
    if_reload = True
    print("已重新加载，请确认：")
    with open(file_name, 'r', encoding='utf8') as myfile:
        all_constants = json.load(myfile)
    for c in all_constants:
        print(c, ":", all_constants[c])
    print("不修改请直接Enter，修改后输入reload重新加载")
    if input() == "reload":
        return if_reload, all_constants
    else:
        if_reload = False
        return if_reload, all_constants


def init_all_constants():
    file_name = "all_constants.json"
    print("正在读取配置文件" + file_name + "...")
    all_constants = {}
    with open(file_name, 'r', encoding='utf8') as myfile:
        all_constants = json.load(myfile)
        print("已读取保存的配置，如需修改请打开" + file_name + "手动修改")
        for c in all_constants:
            print(c, ":", all_constants[c])
        print("不修改请直接Enter，修改后输入reload重新加载")
    if input() == "reload":
        while True:
            if_reload, all_constants = reload_json(file_name)
            if not if_reload:
                break
    else:
        pass
    return all_constants
