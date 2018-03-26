#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from datetime import datetime
import json
import struct
import socket

class CarData(object):
    template = 'AAAAEA000130303731313534333133303130303037533231364C323537313130323239000001E2070319051401060B000100000D00100000000000000000000000000100090000000000000000000C000000000000000000000000000000000000000000000000000000000000000D000000000000000000000000000000000000000000000000000000000000001F000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000210510000009002C03002100000001003200000000000000000000000000000024F9EEEE' 
    def __init__(self):
        self.prefix = 'AAAA' 
        self.package_len = 'AA00'
        self.package_type = '01'
        self.device_id = '30303131313130323036303930303031'
        self.station_number = '473130324C32303631323032323500' 
        self.error_code = '00' # 设备硬件错误码，正常
        self.survey_content = '01' # 调查内容，调查所有项目（不含预留字段）

        self.year = 'E207' # 年份，2018 年 
        self.month = '03' # 月份，3 月
        self.date = '16'  # 日，22 日
        self.period = '05' # 交通数据处理周期，5 分钟
        self.period_cnt = '9000' # 时间序号，第 144 个交通数据处理周期
        self.lane_num = '04' # 车道数，双向 4 个车道

        self.lane_id = '0B' # 11，上行第 1 车道数据开始标志 0B换算成十进制数为11 也就是上行的1车道以后每个车道加1为下一车道 如0B  0C  0D  0E  0F 下行车道从1F开始 1f十进制为31  如 1F  20  21  22  23 车道号 15.33  跟车百分比，51%  //跟车百分比设定一个时间当相邻两辆车通过同一车道时间差小于设定的时间时 那么计算加1 否则不变当一个周期结束时 计算出 在设定时间内通过检测点车辆的总和除以周期内单车道过车的总数（四舍五入摩托除外）
        self.track = '33' #  跟车百分比，51%  跟车百分比设定一个时间当相邻两辆车通过同一车道时间差小于设定的时间时 那么计算加1 否则不变当一个周期结束时 计算出 在设定时间内通过检测点车辆的总和除以周期内单车道过车的总数（四舍五入摩托除外）
        self.head_distance = '1900' # 平均车头间距，25 米（所有的都是在同一个车道的基础上进行计算）设备检测出每辆车的车间距算出平均值
        self.time_occupancy = '2A' # 16.时间占有率，42% 每辆车经过测试点所用时间的总和除以周期
        self.minibus_num= '0000' # 中小客车交通量，0 辆
        self.minibus_speed = '00' #  中小客车平均地点车速，0，无交通量时以 0 填充
        self.minitruck_num = '0300' #  小型货车交通量，3 辆
        self.minitruck_speed = '53' # 小型货车平均地点车速 83 公里/ 小时
        self.bigbus_num= '0300' # 03 00  大客车交通量，3 辆
        self.bigbus_speed = '66' # 66  大客车平均地点车速，102 公里/ 小时
        self.mediumtruck_num = '0200' #  中型货车交通量，2 辆
        self.mediumtruck_speed = '68' # 中型货车平均地点车速，104 公里/ 小时
        self.bigtruck_num= '0000' # 大型货车交通量，0 辆
        self.bigtruck_speed = '00' # 大型货车平均地点车速，0，无交通量时以 0 填充
        self.heavytruck_num= '0000' # 特大型货车交通量，2 辆
        self.heavytruck_speed = '00' #  特大型货车平均地点车速，97 公里/ 小时
        self.containertruck_num = '0000' # 集装箱车交通量，0 辆
        self.containertruck_speed = '00' #  集装箱车平均地点车速，0，无交通量时以 0 填充
        self.tractor_num = '0000' # 拖拉机交通量，0 辆
        self.tractor_speed = '00' # 拖拉机平均地点车速，0，无交通量时以 0 填充
        self.motor_num = '0000' # 摩托车交通量，0 辆
        self.motor_speed = '00' # 摩托车平均地点车速，0，无交通量时以 0 填充

        self.crc = 'EO9F' # CRC 校验（循环冗余校验）结果 橙色的字是crc需要校验的 
        self.suffix = 'EEEE' # 个字节的时间间隔的帧尾


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



def test(argv):
    print 'test'
    cardata = CarData()
    print cardata.template[0:2].decode('hex')

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
    sys.exit(test1(sys.argv))
