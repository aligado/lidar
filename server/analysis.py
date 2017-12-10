# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: alpc32
# Date: 2017-09-12 22:29:40
# Last Modified by:   alpc32
# Last Modified time: 2017-09-12 22:29:40

import time
import math


class CarInfo(object):
    """
    frameinfo object
    """
    threshold_num = 5
    threshold_height = 10

    def __init__(self, id):
        self.info_list = []
        self.horizon_line = 0
        self.under_cnt = 0
        self.id = id

    def insert_frame_info(self, height, width=0):
        height = self.horizon_line - height
        self.info_list.append(height)
        print('insert ', height)
        print('insert ', self.info_list)
        # print(height)
        if height < self.threshold_height:
            self.under_cnt += 1
            if self.under_cnt >= self.threshold_num:
                res = self.car_analysis(self.info_list)
                self.info_list = []
                self.under_cnt = 0
                return res
        else:
            self.under_cnt = 0
        return 'null'

    def car_analysis(self, info_list):
        print('id info_list', self.id, info_list)
        info_len = len(info_list)
        # return
        begin = 0
        end = info_len - self.threshold_num
        while begin<info_len and info_list[begin] < self.threshold_height:
            begin += 1
        print('begin end', begin, end)
        if begin+self.threshold_num < end:
            info_list = info_list[begin:end]
            info_len = len(info_list)
            average_height = 0
            max_height = 0
            for height in info_list:
                average_height += height
                max_height = max(max_height, height)
            average_height /= info_len
            print('average_height', average_height)
            print('analysis_list', info_list)
            print('revolution', end-begin)
            return {
                'average_height': average_height,
                'info_list': info_list,
                'revolution': end-begin,
            }
        return 'null'


    def analysis_height(self, info_list):
        pass



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
