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
import numpy as np
import cv2
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
        "index",
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
        name = log_file.split('.')[0]
        image_floder_path = os.path.join(path, name)
        if not os.path.exists(image_floder_path):
            os.makedirs(image_floder_path)
        csv_file_path = os.path.join(path, name+'.csv')
        with open(log_file_path, 'r+') as fp:
            content = json.loads(fp.read())
            for car_index, car_info in enumerate(content):
                info_list = car_info['info_list']
                car_info['index'] = car_index
                image_content = np.zeros((720, 1280, 3), np.uint8)
                print 'car_draw'
                step = 30
                for index, y in enumerate(info_list):
                    x = step*index+2
                    y = 720 - y*2
                    image_content[ y:y+1, x:x+1] = (0, 0, 255)
                # cv2.imshow('cvcar', image_content)

                print car_index, os.path.join(image_floder_path, str(car_index)+'.png')
                cv2.imwrite(os.path.join(image_floder_path, str(car_index)+'.png'), image_content)
                k = cv2.waitKey(20)
            with open(csv_file_path, 'w+') as f:
                writer = csv.DictWriter(f, headers)
                writer.writeheader()
                writer.writerows(content)

            

def cli(argv):
    """
    """
    print(argv)
    add_data('/media/psf/share/lidar/main/out')

if __name__ == '__main__':
    cli(sys.argv)
