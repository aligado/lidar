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
import json
import math
from multiprocessing import Queue

# test_thread = True
# frame_info_queue = Queue()
# error_frame = 0
queue = Queue()

PI = math.pi

class LidarMsg(object):
    scancfg = "sRN LMPscancfg"
    scandata = "sRN LMDscandata"
    scandata1 = "sEN LMDscandata 1"
    scandata0 = "sEN LMDscandata 0"

def load_config(path):
    f = open(path, 'r+')
    conf = json.load(f)
    f.close()

    #print type(u'1')
    for i in conf:
        if type(conf[i]) == type(u'1'):
            conf[i] = conf[i].encode('utf-8')
    return conf

def hexstr2int(hex_int):
	return c_int32(int(hex_int, 16)).value

class AllConfig(object):
    """
    读取配置文件所有数据
    """
    lidar_height = 0 # 雷达高度
    lane_num = 0 # 车道数量
    lane_min = [0]*6 # 车道边界最小值
    lane_max = [0]*6 # 车道边界最大值
    lane_horizon = [0]*6 # 车道水平线相对倒装雷达
    threshold_num = 2# 间隔阈值
    threshold_height = 33 # 车辆触发高度阈值
    lidar_fix_angle = 0 # 雷达修正角度
    unuse_height = 0
    lidar_hz = 0
    lidar_resolution = 0
    lidar_start_angle = 0
    lidar_end_angle = 0
    host = '192.168.0.1'
    port = 2111
    bufsize = 2048
    car_threshold = 60
    ftp_path = ''
    server_ip = ''
    server_port = ''
    device_id = ''
    station_number = ''

    @staticmethod
    def read_config_file(config_file_path="lidar.json"):
        #print temp_conf
        temp_conf = load_config(config_file_path)
        print 'temp_conf', temp_conf
        AllConfig.lane_max = temp_conf['lane_max']
        AllConfig.lane_num = temp_conf['lane_num']
        AllConfig.lane_min = temp_conf['lane_min']
        AllConfig.lane_horizon = temp_conf['lane_horizon']
        AllConfig.threshold_height = temp_conf['threshold_height']
        AllConfig.threshold_num = temp_conf['threshold_num']
        AllConfig.unuse_height = temp_conf['unuse_height']
        AllConfig.lidar_fix_angle = temp_conf['lidar_fix_angle']
        AllConfig.lidar_start_angle = temp_conf['lidar_start_angle']
        AllConfig.lidar_end_angle = temp_conf['lidar_end_angle']
        AllConfig.lidar_resolution = temp_conf['lidar_resolution']
        AllConfig.lidar_height = temp_conf['lidar_height']
        AllConfig.lidar_hz = temp_conf['lidar_hz']
        AllConfig.local_path = temp_conf['localpath']
        AllConfig.host = temp_conf['host']
        AllConfig.port = temp_conf['port']
        AllConfig.server_ip = temp_conf['server_ip']
        AllConfig.server_port = temp_conf['server_port']
        AllConfig.bufsize = temp_conf['bufsize']
        AllConfig.car_threshold = temp_conf['car_threshold']
        AllConfig.device_id = temp_conf['device_id']
        AllConfig.station_number = temp_conf['station_number']
        print AllConfig.__dict__


def test(args):
    AllConfig.read_config_file()
    pass

if __name__ == '__main__':
    import sys
    sys.exit(test(sys.argv))
