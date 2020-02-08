# coding:gbk
'''
Author:       ����Joker
Purpose:
Date:          2020��2��2��
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
    # ����
    wifi_pswd = ""
    # ����
    average_speed = 0
    # ����
    packet_loss_rate = 100
    # ������
    average_time = 999
    # ƽ������ʱ��

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
        # ���ӳɹ���ʼ������ٺ�����
        average_speed = sa.calculate_average_speed(5)
        packet_loss_rate, average_time = qa.get_quality(ip_or_url)
        my_network.set_speed_quality(average_speed, packet_loss_rate, average_time)

        print(my_network.wifi_SSID + '��ǰ������״���� ')
        print("���٣�", average_speed, "kb/s")
        print("�����ʣ�", packet_loss_rate, '%')
        print("ƽ���ӳ٣�", average_time, "ms")
        print('****************************************')
        return True, my_network
    else:
        return False, my_network


def only_test_wifi(iface, my_network, ip_or_url):
    # �����л�ʱ�����⵱ǰ���ٺ�����

    average_speed = sa.calculate_average_speed(5)
    packet_loss_rate, average_time = qa.get_quality(ip_or_url)
    my_network.set_speed_quality(average_speed, packet_loss_rate, average_time)

    print(my_network.wifi_SSID + '��ǰ������״���� ')
    print("���٣�", average_speed, "kb/s")
    print("�����ʣ�", packet_loss_rate, '%')
    print("ƽ���ӳ٣�", average_time, "ms")
    print('****************************************')


def max_retry_connect(max_retry_time, iface, my_network, ip_or_url):
    for i in range(max_retry_time):
        # ��������max_retry_time��
        if_connected, my_network = change_and_test_wifi(iface, my_network, ip_or_url)
        # ������������ʼ����ƽ�����١������ʺ�ƽ���ӳ�
        if(if_connected):
            break
    else:
        print(max_retry_time, "��ʧ�ܣ�����������һ������wifi")
