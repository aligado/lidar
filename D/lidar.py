# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: alpc32
# Date: 2017-09-12 22:29:40
# Last Modified by:   alpc32
# Last Modified time: 2017-09-12 22:29:40
import socket
import time
from multiprocessing import Process, Array
from mtools import hexstr2int, queue, AllConfig
from data_process import process_queue


class LidarHandle(object):
    """
    雷达驱动接口
    """
    def __init__(self, ip, port):
        """
        """
        self.ip = ip
        self.port = port
        self.s = {}

    def __del__(self):
        self.s.close()

    def connect(self):
        """
        tcp连接雷达
        """
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.ip, self.port))

        self.s.send("sRN LMPscancfg")
        buf = self.s.recv(1024)
        # print 'buf', buf
        temp_ss = buf.split()
        self.frequency = hexstr2int(temp_ss[2])/100
        self.resolution = hexstr2int(temp_ss[4])*1.0/10000.0
        # self.start_angle = 0
        # self.stop_angle = 180
        self.start_angle = hexstr2int(temp_ss[5])*1.0/10000.0
        self.stop_angle = hexstr2int(temp_ss[6][0:-1])*1.0/10000.0
        print self.__dict__

    def close(self):
        """
        关闭雷达连接
        """
        self.s.close()

    def scandata(self):
        """
        获取单个雷达扫描帧 
        """
        self.s.send("sRN LMDscandata")
        buf = self.s.recv(2048)
        queue.put(buf)

    def open_scandata1(self, ar):
        """
        获取雷达连续扫描数据
        """
        self.s.send("sEN LMDscandata 1")
        while True:
            if ar[0] == 0:
                print "get exit cmd"
                break
            buf = self.s.recv(2048)
            # print buf
            queue.put(buf)

    def close_scandata1(self, ar):
        """
        发送关闭连续获取数据命令
        """
        ar[0] = 0
        self.s.send("sEN LMDscandata 0")


def main(args):
    lidar = LidarHandle(AllConfig.host, AllConfig.port)
    lidar.connect()
    lidar.scandata()

    # print queue.qsize()
    scan_flag = Array('i', 1)
    scan_flag[0] = 1

    # 雷达驱动线程
    scandata1_process = Process(target = lidar.open_scandata1, args = (scan_flag, ))
    scandata1_process.start()

    # tcp队列预处理线程
    queue_process = Process(target = process_queue, args = (scan_flag, ))
    queue_process.start()

    '''
    time.sleep(3600)
    lidar.close_scandata1(scan_flag)
    print queue.qsize()
    '''


def maintest(args):
    AllConfig.read_config_file()

    scan_flag = Array('i', 1)
    scan_flag[0] = 1

    def txt2frame():
        for frame in open('rec.txt'):
            queue.put(frame)
            # print queue.get()
            time.sleep(2)

    # 雷达驱动线程
    scandata1_process = Process(targe=txt2frame)
    scandata1_process.start()

    # tcp队列预处理线程
    queue_process = Process(target=process_queue, args=(scan_flag, ))
    queue_process.start()

    # 分型算法线程
    # analysis_process = Process(target = process_queue, args = (scan_flag, ))
    # analysis_process.start()


def unittest(args):
    """
    模块单元测试
    """
    AllConfig.read_config_file()
    lidar = LidarHandle(AllConfig.host, AllConfig.port)
    lidar.connect()

    scan_flag = Array('i', 1)

    scan_flag[0] = 1
    while True:
        lidar.open_scandata1(scan_flag)
        time.sleep(1)
        lidar.close_scandata1(scan_flag)
        while not queue.empty():
            print queue.get()
        print queue.qsize()

if __name__ == '__main__':
    import sys
    # sys.exit(main(sys.argv))
    # sys.exit(maintest(sys.argv))
    sys.exit(unittest(sys.argv))
