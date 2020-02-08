# coding:gbk
'''
Author:       ����Joker
Purpose:
Date:          2020��2��4��
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
    print("Coded By ����Joker")
    print("����������������ֹ����")
    print("���뿪Դ���������붼�����ڱ��أ�������Ϣ�ռ�")
    print("ע�⣺��֧������SSID")
    print("���ȶϿ���ǰ�����Ա�֤APɨ������ȷ")
    print('****************************************')
    print()

    all_constants = ic.init_all_constants()
    # �������õĳ���

    global wifi
    wifi = pywifi.PyWiFi()
    # �½�wifi����ȫ��ʹ��

    ctw.wireless_card_scan(wifi)
    # ɨ�豾������

    global iface
    iface = wifi.interfaces()[all_constants["INTERFACE_NUMBER"]]
    all_wifi = ctw.wifi_scan(iface)
    for wifi_number in all_wifi:
        print("wifi " + str(wifi_number) + ":  ", end='')
        print(all_wifi[wifi_number])
    # ɨ�豾����������AccessPoint

    avail_wifi_SSID, avail_SSID_pswd = ctw.add_avail_wifi(all_wifi)

    all_my_network = []
    # ������е�MyNetWork����
    for avail_wifi in avail_wifi_SSID:
        SSID = avail_wifi_SSID[avail_wifi]
        wifi_SSID = SSID
        wifi_pswd = avail_SSID_pswd[SSID]
        # �õ���ǰ����wifi��SSID��pswd
        my_network = wc.MyNetwork(wifi_SSID, wifi_pswd)
        # ����һ��MyNetwork����
        all_my_network.append(my_network)

    for my_network in all_my_network:
        # ���Ȱ�ȫ����wifi������һ�飬��ʼ�����ٶȵ�����
        wc.max_retry_connect(all_constants["MAX_RETRY_TIME"], iface, my_network, all_constants["IP_OR_URL"])

    all_my_network.sort(key=lambda my_network: (my_network.packet_loss_rate, my_network.average_time))
    # Ȼ�󰴶����ʺ�ƽ���ӳ�˳������
    wc.max_retry_connect(all_constants["MAX_RETRY_TIME"], iface, all_my_network[0], all_constants["IP_OR_URL"])
    # ���ӵ���ǰ����wifi

    while True:
        # Ȼ��ÿ����һ������������ѡ�����ŵ�wifi������

        current_best_wifi = all_my_network[0]
        # ��ǰ���ӵ�����wifi
        wc.only_test_wifi(iface, current_best_wifi, all_constants["IP_OR_URL"])
        # ��⵱ǰ����������

        next_best_wifi = all_my_network[1]
        # ���Ҫ�л����ȿ��ǵ�ǰ�Ĵ���wifi

        if_change = False
        # �Ƿ��л�������wifi

        if current_best_wifi.packet_loss_rate > next_best_wifi.packet_loss_rate:
            # ��ԱȽ�
            # �����ǰ�����ʸ����л�
            if_change = True
        elif current_best_wifi.packet_loss_rate == next_best_wifi.packet_loss_rate:
            # �綪������ͬ
            if current_best_wifi.average_time - next_best_wifi.average_time > all_constants["MAX_DIFFERENCE_DELAY"]:
                # ����ʱ�Ĳ�ֵ�������������ֵ����
                if_change = True

        if current_best_wifi.packet_loss_rate > all_constants["ALLOWED_MAX_PACKET_LOSS_RATE"]:
            # ���ԱȽϣ��Ƿ񳬹��������󶪰���
            # ��ֹ����żȻ���ʹ��һֱ�����л�����wifi
            if_change = True
        elif current_best_wifi.average_time > all_constants["ALLOWED_MAX_DELAY"]:
            # ��ʱ������������ֵ
            if_change = True

        if(if_change):
            # ����Ҫ�л�
            print("�����л����������磺", next_best_wifi.wifi_SSID)
            wc.max_retry_connect(all_constants["MAX_RETRY_TIME"], iface, next_best_wifi, all_constants["IP_OR_URL"])
            # �л�������wifi
            all_my_network.sort(key=lambda my_network: (my_network.packet_loss_rate, my_network.average_time))
            # ������
        else:
            print("�����л�������", all_constants["SLEEP_TIME"], "��")
            time.sleep(all_constants["SLEEP_TIME"])
