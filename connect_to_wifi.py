# coding:gbk
'''
Author:       无名Joker
Purpose:
Date:          2020年2月1日
Arguments:
Outputs:
Dependencies:

History:
--------------------------------------------------------------
Date:
Author:
Modification:
--------------------------------------------------------------
'''
import pywifi
import time
from pywifi import *
import json


def wireless_card_scan(wifi):
    # 传入wifi对象，查看本机所有网卡的状态
    for i in range(len(wifi.interfaces())):
        print("网卡" + str(i) + "： " + wifi.interfaces()[i].name() + " 状态： ", end='')
        if wifi.interfaces()[i].status() == const.IFACE_DISCONNECTED:
            print("DISCONNECTED")
        elif wifi.interfaces()[i].status() == const.IFACE_SCANNING:
            print("SCANNING")
        elif wifi.interfaces()[i].status() == const.IFACE_INACTIVE:
            print("INACTIVE")
        elif wifi.interfaces()[i].status() == const.IFACE_CONNECTING:
            print("CONNECTING")
        elif wifi.interfaces()[i].status() == const.IFACE_CONNECTED:
            print("CONNECTED")


def wifi_scan(iface):
    # 扫描指定网卡可连接的wifi，默认使用第一张
    iface.scan()
    print("正在扫描附近AP...")
    time.sleep(2)
    wifi_results = iface.scan_results()
    all_wifi = {}
    for i in range(len(wifi_results)):
        all_wifi[i] = wifi_results[i].ssid
    if (len(wifi_results) == 0):
        print("No Available wifi")
    return all_wifi


def add_avail_wifi(all_wifi):
    # 添加可用的wifi
    print("输入数个可用wifi的序号(空格分割)建立可用wifi组，示例：0 1 2")
    avail_wifi_number = list(map(int, input().split()))
    avail_wifi_SSID = {}
    file_name = 'SSID_password.json'

    for awn in avail_wifi_number:
        avail_wifi_SSID[awn] = all_wifi[awn]
        # 将所有 序号：SSID 的键值对添加到字典avail_wifi_SSID中

    avail_SSID_pswd = {}
    with open(file_name, 'r') as myfile:
            avail_SSID_pswd = json.load(myfile)
            print("已读取保存的密码，如需修改请打开" + file_name + "手动修改")
            print('****************************************')

    append_new_wifi = False
    # 是否添加了新的可用wifi

    for awn in avail_wifi_number:
        if avail_wifi_SSID[awn] not in avail_SSID_pswd:
            # 如果未保存过此wifi的 SSID: 密码
            avail_SSID_pswd[avail_wifi_SSID[awn]] = input("输入" + avail_wifi_SSID[awn] + "的密码：")
            # 将新的 SSID：密码 的键值对添加到字典avail_SSID_pswd中
            append_new_wifi = True
    if append_new_wifi:
        save_yn = input("是否要保存新的 SSID: 密码？y/n ")
        if_save = False
        if save_yn == 'y':
            if_save = True
        if(if_save):
            with open(file_name, 'w') as myfile:
                json.dump(avail_SSID_pswd, myfile)
                print("密码已保存，如需修改请打开" + file_name + "手动修改")
                print('****************************************')
    return avail_wifi_SSID, avail_SSID_pswd


def connect_to(iface, wifi_SSID, wifi_pswd):
    print("正在尝试连接到", wifi_SSID)
    profile = pywifi.Profile()
    profile.ssid = wifi_SSID
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = wifi_pswd
    profile = iface.add_network_profile(profile)
    iface.connect(profile)
    time.sleep(2)
    # 程序休眠时间2秒；如果没有此句，则会打印连接失败，因为它需要一定的检测时间

    if_connected = False
    if iface.status() == const.IFACE_CONNECTED:
        print("连接成功")
        if_connected = True
    else:
        print("连接失败")
    return if_connected
