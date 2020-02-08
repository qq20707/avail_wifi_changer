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


import re
import subprocess
import time


class LinkState(object):
    def __init__(self):
        pass

    def get_time(self):
        # ��ȡ��ǰʱ��
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

    def get_link_state(self, my_input):
        # ����ping����
        ping_process = subprocess.Popen(("ping %s" % my_input),
             stdin=subprocess.PIPE,
             stdout=subprocess.PIPE,
             stderr=subprocess.PIPE,
             shell=True)

        ping_out = ping_process.stdout.read().decode('gbk')
        # �õ�ping�ķ��ؽ��
        return ping_out


def data_wash(ping_out):
    # ��ping�Ľ����������ϴ

    packet_loss_str = re.findall("��ʧ.*?��ʧ", ping_out)[0]
    # ʹ��?������ƥ��
    average_time_str = re.findall("ƽ��.*?ms", ping_out)[0]

    packet_loss_rate = re.findall("\(.*?%", packet_loss_str)[0].replace("(", "").replace("%", "")
    # ���ĸ����Ķ����ʣ���ȡֵΪ0��25��50��75��100
    average_time = average_time_str.replace("ƽ��", "").replace("=", "").replace("ms", "").strip()
    # ƽ������ʱ��

    return int(packet_loss_rate), int(average_time)


def get_quality(ip_or_url):
    # ����Ҫping��ip��url�����ض����ʺ�ƽ������ʱ��
    ls_obj = LinkState()
    ping_out = ls_obj.get_link_state(ip_or_url)
    packet_loss_rate, average_time = data_wash(ping_out)
    return packet_loss_rate, average_time
