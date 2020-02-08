# coding:gbk
'''
Author:       ����Joker
Purpose:
Date:          2020��2��1��
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
    # ����wifi���󣬲鿴��������������״̬
    for i in range(len(wifi.interfaces())):
        print("����" + str(i) + "�� " + wifi.interfaces()[i].name() + " ״̬�� ", end='')
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
    # ɨ��ָ�����������ӵ�wifi��Ĭ��ʹ�õ�һ��
    iface.scan()
    print("����ɨ�踽��AP...")
    time.sleep(2)
    wifi_results = iface.scan_results()
    all_wifi = {}
    for i in range(len(wifi_results)):
        all_wifi[i] = wifi_results[i].ssid
    if (len(wifi_results) == 0):
        print("No Available wifi")
    return all_wifi


def add_avail_wifi(all_wifi):
    # ��ӿ��õ�wifi
    print("������������wifi�����(�ո�ָ�)��������wifi�飬ʾ����0 1 2")
    avail_wifi_number = list(map(int, input().split()))
    avail_wifi_SSID = {}
    file_name = 'SSID_password.json'

    for awn in avail_wifi_number:
        avail_wifi_SSID[awn] = all_wifi[awn]
        # ������ ��ţ�SSID �ļ�ֵ����ӵ��ֵ�avail_wifi_SSID��

    avail_SSID_pswd = {}
    with open(file_name, 'r') as myfile:
            avail_SSID_pswd = json.load(myfile)
            print("�Ѷ�ȡ��������룬�����޸����" + file_name + "�ֶ��޸�")
            print('****************************************')

    append_new_wifi = False
    # �Ƿ�������µĿ���wifi

    for awn in avail_wifi_number:
        if avail_wifi_SSID[awn] not in avail_SSID_pswd:
            # ���δ�������wifi�� SSID: ����
            avail_SSID_pswd[avail_wifi_SSID[awn]] = input("����" + avail_wifi_SSID[awn] + "�����룺")
            # ���µ� SSID������ �ļ�ֵ����ӵ��ֵ�avail_SSID_pswd��
            append_new_wifi = True
    if append_new_wifi:
        save_yn = input("�Ƿ�Ҫ�����µ� SSID: ���룿y/n ")
        if_save = False
        if save_yn == 'y':
            if_save = True
        if(if_save):
            with open(file_name, 'w') as myfile:
                json.dump(avail_SSID_pswd, myfile)
                print("�����ѱ��棬�����޸����" + file_name + "�ֶ��޸�")
                print('****************************************')
    return avail_wifi_SSID, avail_SSID_pswd


def connect_to(iface, wifi_SSID, wifi_pswd):
    print("���ڳ������ӵ�", wifi_SSID)
    profile = pywifi.Profile()
    profile.ssid = wifi_SSID
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = wifi_pswd
    profile = iface.add_network_profile(profile)
    iface.connect(profile)
    time.sleep(2)
    # ��������ʱ��2�룻���û�д˾䣬����ӡ����ʧ�ܣ���Ϊ����Ҫһ���ļ��ʱ��

    if_connected = False
    if iface.status() == const.IFACE_CONNECTED:
        print("���ӳɹ�")
        if_connected = True
    else:
        print("����ʧ��")
    return if_connected
