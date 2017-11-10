# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: alpc32
# Date: 2017-09-12 22:29:40
# Last Modified by:   alpc32
# Last Modified time: 2017-09-12 22:29:40


import socket
import time
import sys
import gzip
from multiprocessing import Process, Array
from mtools import hexstr2int, queue, AllConfig
from frame import process_frame
from datetime import datetime

__author__ = 'alpc32'
__version__ = '0.1'
__progname__ = 'lidar'

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
        print 'buf', buf
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
                return
            buf = self.s.recv(2048)
            # print buf
            queue.put(buf)

    def close_scandata1(self, ar):
        """
        发送关闭连续获取数据命令
        """
        ar[0] = 0
        self.s.send("sEN LMDscandata 0")


def main():
    AllConfig.read_config_file()
    lidar = LidarHandle(AllConfig.host, AllConfig.port)
    lidar.connect()

    # print queue.qsize()
    scan_flag = Array('i', 1)
    scan_flag[0] = 1

    # 雷达驱动线程
    scandata1_process = Process(target=lidar.open_scandata1, args=(scan_flag, ))
    scandata1_process.start()

    # tcp队列预处理线程
    frame_process = Process(target=process_frame, args=(scan_flag, ))
    frame_process.start()

    time.sleep(20)
    lidar.close_scandata1(scan_flag)
    print queue.qsize()


def frametest():
    AllConfig.read_config_file()

    scan_flag = Array('i', 1)
    scan_flag[0] = 1

    def txt2frame():
        for frame in open('rec.txt'):
            queue.put(frame)
            time.sleep(1)
            # print queue.get()
            # return

    # 雷达驱动线程
    scandata1_process = Process(target=txt2frame)
    scandata1_process.start()

    # tcp队列预处理线程
    frame_process = Process(target=process_frame, args=(scan_flag, ))
    frame_process.start()

    # 分型算法线程
    # analysis_process = Process(target = process_queue, args = (scan_flag, ))
    # analysis_process.start()


def unittest():
    """
    模块单元测试
    """
    AllConfig.read_config_file()
    lidar = LidarHandle(AllConfig.host, AllConfig.port)
    lidar.connect()
    
    def print_queue(ar):
        while True:
            while not queue.empty():
                print queue.get()
                print ""
            if ar[0] == 0:
                return
            time.sleep(0.2)

    # print queue.qsize()
    scan_flag = Array('i', 1)
    while True:
        scan_flag[0] = 1
        scandata1_process = Process(target=lidar.open_scandata1,
                                    args=(scan_flag, ))
        scandata1_process.start()

        frame_process = Process(target=process_frame, args=(scan_flag, ))
        frame_process.start()
       
        # print_process = Process(target=print_queue, args=(scan_flag, ))
        # print_process.start()

        time.sleep(36000)
        lidar.close_scandata1(scan_flag)
        time.sleep(60)


def get_one_frame():
    AllConfig.read_config_file()
    lidar = LidarHandle(AllConfig.host, AllConfig.port)
    lidar.connect()
    for i in range(0, 3):
        lidar.scandata()
    # f = open('one_frame.txt', 'w+')
    scan_flag = Array('i', 1)
    scan_flag[0] = 1
    process_frame(scan_flag)
    while not queue.empty():
        print queue.get()
        print ""

def record_lidar_frame():
    """
    雷达帧保存到本地
    """
    AllConfig.read_config_file()
    lidar = LidarHandle(AllConfig.host, AllConfig.port)
    lidar.connect()
    frame_num = 15000

    def print_queue(ar):
        while True:
            f_name = datetime.now().strftime("%Y%m%d%H%M%S")
            fp = gzip.open('out/'+f_name+'.txt.gz', 'wb')
            fp_cnt = 0
            while fp_cnt < frame_num:
                while (not queue.empty()) and (fp_cnt < frame_num):
                    if fp_cnt % 100 == 0:
                        print "get_frame ", fp_cnt
                    fp.write(queue.get())
                    fp.write('\n')
                    fp_cnt += 1
                    if ar[0] == 0:
                        fp.close()
                        return
                if fp_cnt >= frame_num:
                    print f_name, 'close'
                    fp.close()
                    break
            time.sleep(1)

    # print queue.qsize()
    scan_flag = Array('i', 1)
    scan_flag[0] = 1
    scandata1_process = Process(target=lidar.open_scandata1,
                                args=(scan_flag, ))
    scandata1_process.start()

    record_process = Process(target=print_queue, args=(scan_flag, ))
    record_process.start()

    time.sleep(3600)
    lidar.close_scandata1(scan_flag)
    time.sleep(3)

def cli(argv):
    """
    """
    print(argv)
    if argv[1] == 'record':
        record_lidar_frame()


if __name__ == '__main__':
    # import sys
    # sys.exit(get_one_frame(sys.argv))
    # sys.exit(main(sys.argv))
    # sys.exit(maintest(sys.argv))
    # sys.exit(frametest(sys.argv))
    # sys.exit(unittest(sys.argv))
    cli(sys.argv)
