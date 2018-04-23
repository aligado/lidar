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
import csv
import json

__author__ = 'alpc32'
__version__ = '1.0'
__progname__ = 'lidar'

def add_data(path):
    """
    添加log数据
    """
    car_log_list = []
    log_file_list = os.listdir(path)

    headers = [
        "revolution",
        "lane_id",
        "max_height",
        "average_q",
        "info_list",
        "average_height"
    ]

    for log_file in log_file_list:
        if log_file.find('.json') == -1:
            continue
        log_file_path = os.path.join(path, log_file)
        csv_file_path = log_file_path+'.csv'
        with open(log_file_path, 'r+') as fp:
            content = fp.read()
            with open(csv_file_path, 'w+') as f:
                writer = csv.DictWriter(f, headers)
                writer.writeheader()
                writer.writerows(json.loads(content))

def cli(argv):
    """
    """
    print(argv)
    add_data('/media/psf/share/lidar/main/out')

if __name__ == '__main__':
    cli(sys.argv)
