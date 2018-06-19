#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from datetime import datetime
import json
import struct
import socket
import binascii
import time

from util import AllConfig, DataBuf

def ten2hex(num, hex_len = None):
    res = ""
    while num:
        temp = num % 256
        temp = hex(temp)[2:]
        while len(temp) < 2:
            temp = "0" + temp
        res += temp
        num //= 256
    if hex_len:
        while hex_len > len(res):
            res = res + '0'
    return res


convert = binascii.b2a_hex

class CarData(object):
    def __init__(self):
        self.device_id = AllConfig.device_id  # '0011110206090001'
        # self.device_id = "0021140306120001"  # '0011110206090001'
        self.station_number = AllConfig.station_number  # 'G102L206120225'
        # self.station_number = "S227J205320584" # 'G102L206120225'
        self.now_mess = [
            "AAAA",  # 0 前缀
            "EA00",  # 1 包长度
            "01",  # 2 包类型
            "",  # 3 设备ID 0011110206090001
            "",  # 4 站点号
            "00",  # 5 设备硬件错误码
            "01",  # 6 调查内容，调查所有项目
            "E207",  # 7 年份
            "03",  # 8 月份
            "19",  # 9 日期
            "05",  # 10 交通数据处理周期
            "7100",  # 11 时间序号
            "06",  # 12 车道数
            "0B00000000000000000000000000000000000000000000000000000000000000", # 13
            "0C00000000000000000000000000000000000000000000000000000000000000", # 14
            "0D00000000000000000000000000000000000000000000000000000000000000", # 15
            "1F00000000000000000000000000000000000000000000000000000000000000", # 16
            "2000000000000000000000000000000000000000000000000000000000000000", # 17
            "2100000000000000000000000000000000000000000000000000000000000000", # 18
            "24F9",
            "EEEE"
        ]
        self.now_mess[3] = convert(self.device_id)
        print 'device_id', self.now_mess[3]
        self.now_mess[4] = convert(self.station_number)
        while len(self.now_mess[4]) < 30:
            self.now_mess[4] += '00'

    def pack_message(self, mess):
        """
        打包message
        """
        self.now_mess[7] = ten2hex(mess['year'], 4)
        print 'year', self.now_mess[7]
        self.now_mess[8] = ten2hex(mess['month'], 2)
        print 'month', self.now_mess[8]
        self.now_mess[9] = ten2hex(mess['day'], 2)
        print 'day', self.now_mess[9]
        minutes = mess['hour']*60 + mess['minute']
        periods = minutes // 5 + 1
        self.now_mess[11] = ten2hex(periods, 4)
        print 'periods', self.now_mess[11]
        for index, car_mess in enumerate(mess['car']):
            print index, car_mess
            num_list = car_mess['num']
            spd_list = car_mess['spd']
            temp = self.now_mess[13+index]
            self.now_mess[13+index] = temp[0:10]
            for j, num in enumerate(num_list):
                # self.now_mess[13+index] += ten2hex(car_num, 4) + '00'
                spd = spd_list[j]
                self.now_mess[13+index] += ten2hex(num, 4) + ten2hex(spd, 2)
        return ''.join(self.now_mess)


    def hex(self):
        data = self.template
        return data.decode('hex')

    def write_buf(self, buf):
        pass
    
    def tcp_client(self, buf):
        pass

def msg_server():
    while True:
        if DataBuf.flag[0] == 0:
            print "get exit cmd"
            return
        while not DataBuf.res.empty():
            car_mess = DataBuf.res.get()
            send_msg(car_mess)
        time.sleep(10)

def send_msg(car_mess):
    """
    发送结果数据到指定服务器
    """
    cardata = CarData()
    mess = {
        'year': 2018,
        'month': 4,
        'day': 11,
        'hour': 8,
        'minute': 6,
        'car': [
            {
                'total': 1
            },
            {
                'total': 2
            },
            {
                'total': 3
            },
            {
                'total': 3
            },
            {
                'total': 2
            },
            {
                'total': 1
            },
        ]
    }
    now_time = datetime.now()
    mess['year'] = now_time.year
    mess['month'] = now_time.month
    mess['day'] = now_time.day
    mess['hour'] = now_time.hour
    mess['minute'] = now_time.minute

    mess['car'] = car_mess
    temp = cardata.pack_message(mess)
    send_cnt = 0
    ip = AllConfig.server_ip
    port = AllConfig.server_port

    # 尝试10次传送
    while send_cnt < 10:
        try:
            print temp, len(temp) 
            # print cardata.template, len(cardata.template) 
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((ip, port))
            # temp = cardata.template
            s.send(temp.decode('hex'))
            data = s.recv(1024)
            print data.encode('hex')
            s.close()
            break
        except Exception as identifier:
            print identifier, 'Error'
            send_cnt += 1
            time.sleep(5)
    # print cardata.template[0:2].decode('hex')


if __name__ == '__main__':
    import sys
    # sys.exit(test2(sys.argv))
    pass
