# -*- coding: utf-8 -*-
import os
import sys
from cStringIO import StringIO as IO
import json
import gzip
import functools
from lidar import LidarHandle
from mtools import hexstr2int, queue, AllConfig
from multiprocessing import Process, Array, Value, Queue
import time
from frame import read_frame
from analysis import car_analysis

RELEASE_PATH = 'out'
pack = os.path.join


class Handle(object):
    lidar = None
    scan_flag = Array('i', 5)
    scandata1_process = None
    read_process = None
    car_process = None
    frame_queue = queue
    car_queue = Queue()

    web_frame_queue = Queue()
    web_lane_queue = Queue()
    web_car_queue = Queue()

    @classmethod
    def create_scan_process(cls):
        cls.scan_flag[0] = 1

        cls.scandata1_process = Process(target=cls.lidar.open_scandata1,
                                        args=(cls.scan_flag, ))

        cls.scandata1_process.daemon = True
        cls.scandata1_process.start()

    @classmethod
    def create_read_process(cls):
        cls.read_process = Process(target=read_frame,
                                   args=(cls.scan_flag,
                                         cls.frame_queue,
                                         cls.web_frame_queue,
                                         cls.car_queue))
        cls.read_process.daemon = True
        cls.read_process.start()

    @classmethod
    def create_analysis_process(cls):
        cls.car_process = Process(target=car_analysis,
                                  args=(cls.scan_flag,
                                        cls.car_queue,
                                        cls.web_car_queue))
        cls.car_process.daemon = True
        cls.car_process.start()

    @classmethod
    def connect(cls):
        cls.lidar = LidarHandle(AllConfig.host, AllConfig.port)
        cls.lidar.connect()

    @classmethod
    def close_scan_process(cls):
        cls.lidar.close_scandata1(cls.scan_flag)
        cls.lidar.close()
        time.sleep(2)

def system_shutdown():
    """
    关闭雷达持续扫描,断开tcp连接
    """
    # time.sleep(600)
    Handle.close_scan_process()
    print 'close_scan_process'

def system_poweron():
    """
    初始化
    """
    AllConfig.read_config_file()
    Handle.connect()
    Handle.create_scan_process()
    print 'create_scan_process'
    Handle.create_read_process()
    print 'create_read_process'
    Handle.create_analysis_process()
    print 'create_analysis_process'
    '''
    while not Handle.frame_queue.empty():
        print Handle.frame_queue.get()
        print ""
    '''

if __name__ == '__main__':
    system_poweron()
    while True:
        time.sleep(10)
    # app.run(debug=True, host="0.0.0.0", port=8080)
