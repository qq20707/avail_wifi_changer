# coding:gbk
'''
Author:       无名Joker
Purpose:
Date:          2020年2月4日
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
from avail_wifi_changer import connect_to_wifi as ctw
from avail_wifi_changer import wifi_changer as wc
from avail_wifi_changer import init_constants as ic


if __name__ == "__main__":
    print('****************************************')
    print("Coded By 无名Joker")
    print("仅供技术交流，禁止商用")
    print("代码开源，所有密码都保存在本地，不作信息收集")
    print("注意：不支持中文SSID")
    print("请先断开当前连接以保证AP扫描结果正确")
    print('****************************************')
    print()

    all_constants = ic.init_all_constants()
    # 读入配置的常量

    global wifi
    wifi = pywifi.PyWiFi()
    # 新建wifi对象，全局使用

    ctw.wireless_card_scan(wifi)
    # 扫描本机网卡

    global iface
    iface = wifi.interfaces()[all_constants["INTERFACE_NUMBER"]]
    all_wifi = ctw.wifi_scan(iface)
    for wifi_number in all_wifi:
        print("wifi " + str(wifi_number) + ":  ", end='')
        print(all_wifi[wifi_number])
    # 扫描本网卡附近的AccessPoint

    avail_wifi_SSID, avail_SSID_pswd = ctw.add_avail_wifi(all_wifi)

    all_my_network = []
    # 存放所有的MyNetWork对象
    for avail_wifi in avail_wifi_SSID:
        SSID = avail_wifi_SSID[avail_wifi]
        wifi_SSID = SSID
        wifi_pswd = avail_SSID_pswd[SSID]
        # 拿到当前可用wifi的SSID和pswd
        my_network = wc.MyNetwork(wifi_SSID, wifi_pswd)
        # 创建一个MyNetwork对象
        all_my_network.append(my_network)

    for my_network in all_my_network:
        # 首先把全部的wifi都测试一遍，初始化其速度等属性
        wc.max_retry_connect(all_constants["MAX_RETRY_TIME"], iface, my_network, all_constants["IP_OR_URL"])

    all_my_network.sort(key=lambda my_network: (my_network.packet_loss_rate, my_network.average_time))
    # 然后按丢包率和平均延迟顺序排序
    wc.max_retry_connect(all_constants["MAX_RETRY_TIME"], iface, all_my_network[0], all_constants["IP_OR_URL"])
    # 连接到当前最优wifi

    while True:
        # 然后每测试一个都重新排序，选择最优的wifi作连接

        current_best_wifi = all_my_network[0]
        # 当前连接的最优wifi
        wc.only_test_wifi(iface, current_best_wifi, all_constants["IP_OR_URL"])
        # 检测当前的连接质量

        next_best_wifi = all_my_network[1]
        # 如果要切换则先考虑当前的次优wifi

        if_change = False
        # 是否切换到次优wifi

        if current_best_wifi.packet_loss_rate > next_best_wifi.packet_loss_rate:
            # 相对比较
            # 如果当前丢包率高则切换
            if_change = True
        elif current_best_wifi.packet_loss_rate == next_best_wifi.packet_loss_rate:
            # 如丢包率相同
            if current_best_wifi.average_time - next_best_wifi.average_time > all_constants["MAX_DIFFERENCE_DELAY"]:
                # 但延时的差值大于允许的最大差值，切
                if_change = True

        if current_best_wifi.packet_loss_rate > all_constants["ALLOWED_MAX_PACKET_LOSS_RATE"]:
            # 绝对比较，是否超过允许的最大丢包率
            # 防止出现偶然情况使得一直不能切换次优wifi
            if_change = True
        elif current_best_wifi.average_time > all_constants["ALLOWED_MAX_DELAY"]:
            # 延时大于允许的最大值
            if_change = True

        if(if_change):
            # 如需要切换
            print("正在切换至更优网络：", next_best_wifi.wifi_SSID)
            wc.max_retry_connect(all_constants["MAX_RETRY_TIME"], iface, next_best_wifi, all_constants["IP_OR_URL"])
            # 切换到次优wifi
            all_my_network.sort(key=lambda my_network: (my_network.packet_loss_rate, my_network.average_time))
            # 重排序
        else:
            print("无需切换，休眠", all_constants["SLEEP_TIME"], "秒")
            time.sleep(all_constants["SLEEP_TIME"])
