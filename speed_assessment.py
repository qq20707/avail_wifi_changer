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
import psutil
import time


def get_speed_per_deci():
    # ����0.1���ڵ�����
    s1 = psutil.net_io_counters(pernic=True)['WLAN']
    time.sleep(0.1)
    s2 = psutil.net_io_counters(pernic=True)['WLAN']
    result = s2.bytes_recv - s1.bytes_recv
    # �������������λС������λΪ kb/0.1s
    speed_deci = '%.2f' % (result / 1024)
    return speed_deci


def calculate_average_speed(seconds):
    # ����seconds���ڵ�ƽ�����٣���λkb/s
    sum_speed = 0.0
    for s in range(seconds * 10):
        sum_speed += float(get_speed_per_deci())
    average_speed = '%.2f' % (sum_speed / seconds * 10)
    return average_speed
