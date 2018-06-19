#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: alpc32
# Date: 2017-09-12 22:29:40
# Last Modified by:   alpc32
# Last Modified time: 2017-09-12 22:29:40
"""
工具模块
"""

from ctypes import c_int32
from multiprocessing import Queue, Array
import json
import math

PI = math.pi

class DataBuf(object):
    """
    进程间数据缓存
    """
    flag = Array('i', 5)
    frame = Queue()
    car = Queue()
    res = Queue()

class LidarMsg(object):
    """
    雷达命令
    """
    scancfg = "sRN LMPscancfg"
    scandata = "sRN LMDscandata"
    scandata1 = "sEN LMDscandata 1"
    scandata0 = "sEN LMDscandata 0"

def hexstr2int(hex_int):
	return c_int32(int(hex_int, 16)).value


class AllConfig(object):
    """
    读取配置文件所有数据
    """
    lane = []

    threshold_height = 33 # 车辆触发高度阈值
    threshold_num = 2# 间隔阈值
    car_threshold = 60

    lidar_fix_angle = 0 # 雷达修正角度
    lidar_resolution = 0

    local_path = ''
    host = '192.168.0.1'
    port = 2111
    bufsize = 2048

    server_ip = ''
    server_port = ''
    device_id = ''
    station_number = ''

    @staticmethod
    def read_config_file(config_file_path="lidar.json"):

        with open(config_file_path, 'r+') as f:
            temp_conf = json.load(f)
            for i in temp_conf:
                if type(temp_conf[i]) == type(u'1'):
                    temp_conf[i] = temp_conf[i].encode('utf-8')

        print '----------- conf begin --------------'
        print temp_conf
        print '----------- conf end --------------'
        AllConfig.lane = temp_conf['lane']

        AllConfig.threshold_height = temp_conf['threshold_height']
        AllConfig.threshold_num = temp_conf['threshold_num']
        AllConfig.car_threshold = temp_conf['car_threshold']

        AllConfig.lidar_fix_angle = temp_conf['lidar_fix_angle']
        AllConfig.lidar_resolution = temp_conf['lidar_resolution']

        AllConfig.local_path = temp_conf['localpath']
        AllConfig.host = temp_conf['host']
        AllConfig.port = temp_conf['port']
        AllConfig.bufsize = temp_conf['bufsize']

        AllConfig.server_ip = temp_conf['server_ip']
        AllConfig.server_port = temp_conf['server_port']
        AllConfig.device_id = temp_conf['device_id']
        AllConfig.station_number = temp_conf['station_number']

        print AllConfig.__dict__


def test(args):
    AllConfig.read_config_file()

if __name__ == '__main__':
    import sys
    sys.exit(test(sys.argv))
