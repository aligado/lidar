# -*- coding: utf-8 -*-
import os
import sys
import json
import gzip
import functools
import time
from lidar import LidarHandle
from util import AllConfig, DataBuf
from multiprocessing import Process, Array, Value, Queue
from frame import frame_handle
from analysis import car_analysis
from proxy import msg_server

class Handle(object):
    lidar = None

    @classmethod
    def create_scan_process(cls):
        cls.scandata1_process = Process(target=cls.lidar.open_scandata1,
                                        args=())
        cls.scandata1_process.daemon = True
        cls.scandata1_process.start()

    @classmethod
    def create_read_process(cls):
        cls.read_process = Process(target=frame_handle,
                                   args=())
        cls.read_process.daemon = True
        cls.read_process.start()

    @classmethod
    def create_analysis_process(cls):
        cls.car_process = Process(target=car_analysis,
                                  args=())
        cls.car_process.daemon = True
        cls.car_process.start()

    @classmethod
    def create_proxy_process(cls):
        cls.proxy_process = Process(target=msg_server,
                                    args=())
        cls.proxy_process.daemon = True
        cls.proxy_process.start()

    @classmethod
    def connect(cls):
        cls.lidar = LidarHandle(AllConfig.host, AllConfig.port)
        cls.lidar.connect()

    @classmethod
    def close_scan_process(cls):
        cls.lidar.close_scandata1()
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
    启动雷达程序
    """
    DataBuf.flag[0] = 1
    AllConfig.read_config_file()
    Handle.connect()
    Handle.create_scan_process()
    print 'create_scan_process'
    Handle.create_read_process()
    print 'create_read_process'
    Handle.create_analysis_process()
    print 'create_analysis_process'
    Handle.create_proxy_process()
    print 'create_proxy_process'

if __name__ == '__main__':
    system_poweron()
    time.sleep(6000)
    system_shutdown()
    '''
    while True:
        time.sleep(60)
    '''
