# coding:gbk
'''
Author:       ����Joker
Purpose:    ��ʼ�����г���
Date:          2020��2��7��
Arguments:
Outputs:

json�ļ���
�������·ֱ�Ϊ��
�����������
Ĭ���������
����ǰ������������������ӳٲ�ֵ(����Ƶ���л������Ŀ���)
���������ӳ�
�������󶪰���
�����л�ʱ�������ߵ�ʱ��
Ĭ��PING��IP��URL


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
    print("�����¼��أ���ȷ�ϣ�")
    with open(file_name, 'r', encoding='utf8') as myfile:
        all_constants = json.load(myfile)
    for c in all_constants:
        print(c, ":", all_constants[c])
    print("���޸���ֱ��Enter���޸ĺ�����reload���¼���")
    if input() == "reload":
        return if_reload, all_constants
    else:
        if_reload = False
        return if_reload, all_constants


def init_all_constants():
    file_name = "all_constants.json"
    print("���ڶ�ȡ�����ļ�" + file_name + "...")
    all_constants = {}
    with open(file_name, 'r', encoding='utf8') as myfile:
        all_constants = json.load(myfile)
        print("�Ѷ�ȡ��������ã������޸����" + file_name + "�ֶ��޸�")
        for c in all_constants:
            print(c, ":", all_constants[c])
        print("���޸���ֱ��Enter���޸ĺ�����reload���¼���")
    if input() == "reload":
        while True:
            if_reload, all_constants = reload_json(file_name)
            if not if_reload:
                break
    else:
        pass
    return all_constants
