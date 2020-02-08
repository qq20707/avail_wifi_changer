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


import re
import subprocess
import time


class LinkState(object):
    def __init__(self):
        pass

    def get_time(self):
        # 获取当前时间
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

    def get_link_state(self, my_input):
        # 运行ping命令
        ping_process = subprocess.Popen(("ping %s" % my_input),
             stdin=subprocess.PIPE,
             stdout=subprocess.PIPE,
             stderr=subprocess.PIPE,
             shell=True)

        ping_out = ping_process.stdout.read().decode('gbk')
        # 得到ping的返回结果
        return ping_out


def data_wash(ping_out):
    # 对ping的结果作数据清洗

    packet_loss_str = re.findall("丢失.*?丢失", ping_out)[0]
    # 使用?作懒惰匹配
    average_time_str = re.findall("平均.*?ms", ping_out)[0]

    packet_loss_rate = re.findall("\(.*?%", packet_loss_str)[0].replace("(", "").replace("%", "")
    # 发四个包的丢包率，可取值为0、25、50，75、100
    average_time = average_time_str.replace("平均", "").replace("=", "").replace("ms", "").strip()
    # 平均往返时间

    return int(packet_loss_rate), int(average_time)


def get_quality(ip_or_url):
    # 输入要ping的ip或url，返回丢包率和平均往返时间
    ls_obj = LinkState()
    ping_out = ls_obj.get_link_state(ip_or_url)
    packet_loss_rate, average_time = data_wash(ping_out)
    return packet_loss_rate, average_time
