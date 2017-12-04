# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: alpc32
# Date: 2017-09-12 22:29:40
# Last Modified by:   alpc32
# Last Modified time: 2017-09-12 22:29:40

import time
import math
from file_handle import FileHandle
from mtools import queue, frame_info_queue, hexstr2int, AllConfig, PI


class CarInfo(object):
    """
    frameinfo object
    """

    def __init__(self):
        self.info_list = []
        self.under_threshold_num = 0

    def insert_frame_info(self, height, width):
        self.info_list.append((height, width))
        if width < AllConfig.car_threshold:
            self.under_threshold_num += 1
        if self.under_threshold_num >= AllConfig.car_threshold_num:
            self.car_analysis(self.info_list)
            self.info_list = []
            self.under_threshold_num = 0

    def car_analysis(self, info_list):
        info_len = len(info_list)
        begin = 0
        end = info_len - AllConfig.car_threshold_num
        while info_list[begin] < AllConfig.car_threshold:
            begin += 1
        info_list = info_list[begin, end]


def process_frame_info(ar):
    """
    处理帧信息
    """
    # file_handle = FileHandle()
    # frame_cnt = 0
    car_info = []
    for index in range(0, 6):
        car_info.append(CarInfo())

    while True:
        # print 'queuesize', queue.qsize(), 'frame_cnt', frame_cnt
        # 处理frame info queue队列中留存的所有扫描数据
        while not frame_info_queue.empty():
            frame_info = frame_info_queue.get()
            # print buf
            for index in range(0, 6):
                car_info[index].insert(frame_info[index * 2],
                                       frame_info[index * 2 + 1])
        if ar[0] == 0:
            break
        time.sleep(0.1)


def unittest(args):
    """
    单元测试
    """
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(unittest(sys.argv))
