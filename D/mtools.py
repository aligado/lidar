#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: alpc32 
#Date: 2017-09-12 22:29:40 
#Last Modified by:   alpc32 
#Last Modified time: 2017-09-12 22:29:40 

from ctypes import c_int32
import json
from multiprocessing import Queue

test_thread = True
PI = 3.1415926

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
    lane_min = [0]*6
    lane_num = 6
    lane_max = [0]*6
    lidar_height = 800
    lidar_hz = 25
    lidar_resolution = 0.5
    lidar_start_angle = 0
    lidar_end_angle = 0
    ftp_path = ''
    host = '192.168.0.1'
    port = 2111
    bufsize = 2048
    car_threshold = 60

    @staticmethod
    def read_config_file(path="lidar.conf"):
        temp_conf = load_config("lidar.conf")
        #print temp_conf
        AllConfig.lane_max = temp_conf['lane_max']
        AllConfig.lane_num = temp_conf['lane_num']
        AllConfig.lane_min = temp_conf['lane_min']
        AllConfig.lidar_start_angle = temp_conf['lidar_start_angle']
        AllConfig.lidar_end_angle = temp_conf['lidar_end_angle']
        AllConfig.lidar_resolution = temp_conf['lidar_resolution']
        AllConfig.lidar_height = temp_conf['lidar_height']
        AllConfig.lidar_hz = temp_conf['lidar_hz']
        AllConfig.local_path = temp_conf['localpath']
        AllConfig.host = temp_conf['host']
        AllConfig.port = temp_conf['port']
        AllConfig.ftp_path = temp_conf['ftppath']
        AllConfig.bufsize = temp_conf['bufsize']
        AllConfig.car_threshold = temp_conf['car_threshold']
        print AllConfig.__dict__

queue = Queue()
frame_info_queue = Queue()
error_frame = 0
PI = 3.1415926

def test(args):
    AllConfig.read_config_file()
    pass
'''
if __name__ == '__main__':
    import sys
    sys.exit(test(sys.argv))
'''
