# coding:gbk
'''
Author:       无名Joker
Purpose:
Date:          2020年2月2日
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


from avail_wifi_changer import connect_to_wifi as ctw
from avail_wifi_changer import speed_assessment as sa
from avail_wifi_changer import quality_assessment as qa


class MyNetwork():
    wifi_SSID = ""
    # 名称
    wifi_pswd = ""
    # 密码
    average_speed = 0
    # 网速
    packet_loss_rate = 100
    # 丢包率
    average_time = 999
    # 平均往返时间

    def __init__(self, wifi_SSID, wifi_pswd):
        self.wifi_SSID = wifi_SSID
        self.wifi_pswd = wifi_pswd

    def set_speed_quality(self, average_speed, packet_loss_rate, average_time):
        self.average_speed = average_speed
        self.packet_loss_rate = packet_loss_rate
        self.average_time = average_time


def change_and_test_wifi(iface, my_network, ip_or_url):
    if_connected = ctw.connect_to(iface, my_network.wifi_SSID, my_network.wifi_pswd)
    if (if_connected):
        # 连接成功后开始检测网速和质量
        average_speed = sa.calculate_average_speed(5)
        packet_loss_rate, average_time = qa.get_quality(ip_or_url)
        my_network.set_speed_quality(average_speed, packet_loss_rate, average_time)

        print(my_network.wifi_SSID + '当前的网络状况： ')
        print("网速：", average_speed, "kb/s")
        print("丢包率：", packet_loss_rate, '%')
        print("平均延迟：", average_time, "ms")
        print('****************************************')
        return True, my_network
    else:
        return False, my_network


def only_test_wifi(iface, my_network, ip_or_url):
    # 无需切换时仍需检测当前网速和质量

    average_speed = sa.calculate_average_speed(5)
    packet_loss_rate, average_time = qa.get_quality(ip_or_url)
    my_network.set_speed_quality(average_speed, packet_loss_rate, average_time)

    print(my_network.wifi_SSID + '当前的网络状况： ')
    print("网速：", average_speed, "kb/s")
    print("丢包率：", packet_loss_rate, '%')
    print("平均延迟：", average_time, "ms")
    print('****************************************')


def max_retry_connect(max_retry_time, iface, my_network, ip_or_url):
    for i in range(max_retry_time):
        # 尝试连接max_retry_time次
        if_connected, my_network = change_and_test_wifi(iface, my_network, ip_or_url)
        # 如果连接上则初始化其平均网速、丢包率和平均延迟
        if(if_connected):
            break
    else:
        print(max_retry_time, "次失败，尝试连接下一个可用wifi")
