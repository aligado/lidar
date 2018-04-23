# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: alpc32
# Date: 2017-09-12 22:29:40
# Last Modified by:   alpc32
# Last Modified time: 2018年 2月15日 星期四 17时13分31秒 CST


import socket
import time
import sys
import gzip
import os
from multiprocessing import Process, Array
import threading
from mtools import hexstr2int, queue, AllConfig, LidarMsg
from datetime import datetime

__author__ = 'alpc32'
__version__ = '1.0'
__progname__ = 'lidar'


class LidarSimulate(object):
    """
    雷达驱动接口
    """
    def __init__(self, port):
        """
        @port 雷达端口
        @socket 雷达tcp实例
        """
        self.port = port
        self.socket = None
        self.lidar_log_list = []
        self.lidar_log_index = 0
        self.lidar_log_len = 0

    def add_data(self, path):
        """
        添加log数据
        """
        self.lidar_log_list = []
        log_file_list = os.listdir(path)
        for log_file in log_file_list:
            if log_file.find('.txt') == -1:
                continue
            log_file_path = os.path.join(path, log_file)
            with open(log_file_path, 'r+') as fp:
                lines = fp.readlines()
                for line in lines:
                    self.lidar_log_list.append(line.split('\n')[0])
        self.lidar_log_len = len(self.lidar_log_list)
        
        print 'lidar_log_list[0:2]', self.lidar_log_list[0:2]

    def poweron(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.bind(('127.0.0.1', self.port))

        s.listen(5)
        print 'Waiting for connection...'

        def tcplink(sock, addr):
            print 'Accept new connection from %s:%s...' % addr
            '''
            def tcp_send(sock):
                for i in range(100)
                    sock.send('hello')
                    time.sleep(0.1)
                pass
            '''
            while True:
                data = sock.recv(1024)
                print data
                if data == LidarMsg.scandata1:
                    print 'simu scandata1'
                    for line in self.lidar_log_list:
                        print 'line', line[0:20]
                        sock.send(line)
                        time.sleep(0.03)
                    return
                else:
                    sock.send('o')
                time.sleep(0.1)
            sock.close()
            print 'Connection from %s:%s closed.' % addr

        while True:
            # 接受一个新连接:
            sock, addr = s.accept()
            # 创建新线程来处理TCP连接:
            t = threading.Thread(target=tcplink, args=(sock, addr))
            t.daemon = True
            t.start()

def cli(argv):
    """
    """
    print(argv)
    lidar_simulate = LidarSimulate(9999)
    lidar_simulate.add_data('/media/psf/share/lidar/data')
    lidar_simulate.poweron()

if __name__ == '__main__':
    cli(sys.argv)
