#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from datetime import datetime
import json
import struct
import socket
import binascii

def ten2hex(num, hex_len = None):
    res = ""
    while num:
        temp = num % 256
        temp = hex(temp)[2:]
        while len(temp)<2:
            temp = "0" + temp
        res += temp
        num //= 256
    if hex_len:
        while hex_len > len(res):
            res = res + '0'
    return res


convert = binascii.b2a_hex

class CarData(object):
    template = 'AAAAEA000130303731313534333133303130303037533231364C323537313130323239000001E2070319051401060B000100000D00100000000000000000000000000100090000000000000000000C000000000000000000000000000000000000000000000000000000000000000D000000000000000000000000000000000000000000000000000000000000001F000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000210510000009002C03002100000001003200000000000000000000000000000024F9EEEE' 
    sample = [
        "AAAA", #0 前缀 
        "EA00", #1 包长度
        "01", #2 包类型
        "30303731313534333133303130303037", #3 设备ID
        "533231364C32353731313032323900", #4 站点号
        "00", #5 设备硬件错误码
        "01", #6 调查内容，调查所有项目
        "E207", #7 年份
        "03", #8 月份
        "19", #9 日期
        "05", #10 交通数据处理周期
        "7100", #11 时间序号
        "06", #12 车道数
        "0B000100000D0010000000000000000000000000010009000000000000000000", #13 第一个车道数据
        "0C00000000000000000000000000000000000000000000000000000000000000",
        "0D00000000000000000000000000000000000000000000000000000000000000",
        "1F00000000000000000000000000000000000000000000000000000000000000",
        "2000000000000000000000000000000000000000000000000000000000000000",
        "21051000000D002C030021000000010032000000000000000000000000000000",
        "24F9", #-2 CRC校验
        "EEEE" #-1 数据包结尾
    ]
    def __init__(self):
        # print(self.sample[13])
        # print(len(self.sample[13]))
        self.device_id = "0021140306120001" # '0011110206090001'
        # self.device_id = '0011110206090001'
        self.station_number = "S227J205320584" # 'G102L206120225'
        # self.station_number = 'S216L257110229'
        self.now_mess = [
            "AAAA", #0 前缀 
            "EA00", #1 包长度
            "01", #2 包类型
            "", #3 设备ID 0011110206090001
            "", #4 站点号
            "00", #5 设备硬件错误码
            "01", #6 调查内容，调查所有项目
            "E207", #7 年份
            "03", #8 月份
            "19", #9 日期
            "05", #10 交通数据处理周期
            "7100", #11 时间序号
            "06", #12 车道数
            "0B00000000000000000000000000000000000000000000000000000000000000",
            "0C00000000000000000000000000000000000000000000000000000000000000",
            "0D00000000000000000000000000000000000000000000000000000000000000",
            "1F00000000000000000000000000000000000000000000000000000000000000",
            "2000000000000000000000000000000000000000000000000000000000000000",
            "2100000000000000000000000000000000000000000000000000000000000000",
            "24F9",
            "EEEE"
        ]
        self.now_mess[3] = convert(self.device_id)
        print 'device_id', self.now_mess[3]
        self.now_mess[4] = convert(self.station_number)
        while len(self.now_mess[4])<30:
            self.now_mess[4] += '00'

    def pack_message(self, mess):
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
            car_num = car_mess['total']
            temp = self.now_mess[13+index]
            self.now_mess[13+index] = temp[0:10] + ten2hex(car_num, 4) + temp[14:]
        return ''.join(self.now_mess)


    def hex(self):
        data = self.template
        return data.decode('hex')
        '''
        print len(data)
        str2 = ''
        str1 = ''
        while data:
            str1 = data[0:2]
            s = int(str1,16)
            print(str1, s)
            str2 += struct.pack('B',s)
            data = data[2:]
        return str2
        ''' 

    def write_buf(self, buf):
        pass
    
    def tcp_client(self, buf):
        pass

def send_msg(car_mess):
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
    mess['car'] = car_mess
    temp =  cardata.pack_message(mess)
    print temp, len(temp) 
    print cardata.template, len(cardata.template) 
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('121.52.216.242', 3132))
    # temp = cardata.template
    s.send(temp.decode('hex'))
    data = s.recv(1024)
    print data.encode('hex')
    # print cardata.template[0:2].decode('hex')

def test(argv):
    print 'test'
    cardata = CarData()
    # print cardata.template[0:2].decode('hex')

def test2(argv):
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
    temp =  cardata.pack_message(mess)
    print temp, len(temp) 
    print cardata.template, len(cardata.template) 
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('121.52.216.242', 3132))
    # temp = cardata.template
    s.send(temp.decode('hex'))
    data = s.recv(1024)
    print data.encode('hex')
    # print cardata.template[0:2].decode('hex')

def test1(argv):
    print 'test'
    cardata = CarData()
    print cardata.__dict__
    res = cardata.hex()
    print res
    length = 0
    for item in cardata.__dict__:
        print item
        length += len(cardata.__dict__[item])
    # print(length + ((6+8)*9+6+4)*3+8*9)
    print(length + (6*9+6+4)*5)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('121.52.216.242', 3132))
    s.send(res)
    data = s.recv(1024)
    print data.encode('hex')

if __name__ == '__main__':
    import sys
    # sys.exit(test(sys.argv))
    sys.exit(test2(sys.argv))
