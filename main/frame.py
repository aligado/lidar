# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: alpc32
# Date: 2017-09-12 22:29:40
# Last Modified by:   alpc32
# Last Modified time: 2017-09-12 22:29:40

import time
import math
from file_handle import FileHandle
from mtools import queue, frame_info_queue, hexstr2int, AllConfig, PI, error_frame

PI = math.pi 
hex2int = hexstr2int

class CarInfo(object):
    """
    frameinfo object
    处理每个
    """
    threshold_num = AllConfig.threshold_num
    threshold_height = AllConfig.threshold_height

    def __init__(self, id):
        self.info_list = []
        self.horizon_line = 0
        self.under_cnt = 0
        self.id = id

    def insert_frame_info(self, height, width=0):
        height = self.horizon_line - height
        self.info_list.append(height)
        '''
        print('insert', height)
        print('insert', self.info_list)
        '''
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
        # print('id info_list', self.id, info_list)
        info_len = len(info_list)
        begin = 0
        end = info_len - self.threshold_num
        while begin<info_len and info_list[begin] < self.threshold_height:
            begin += 1
        # print('begin end', begin, end)
        if begin+self.threshold_num < end:
            info_list = info_list[begin:end]
            # info_len = len(info_list)
            return {
                'id': self.id,
                'info_list': info_list,
            }
        return 'null'

def get_frame_info(buf, car_info):
    """
    将帧的信息分为6个车道进行处理
    """
    xdata, ydata = [], []
    buf_len = len(buf)
    if buf_len < 26:
        return [], [], [], []

    num_len = hex2int(buf[25])
    # print('len ', num_len)
    end = min(26+num_len, buf_len)
    height = [AllConfig.unuse_height]*6

    for i in range(26, end):
        angle = ((i - 26 + AllConfig.lidar_fix_angle) * 0.5 + 0) * PI / 180.0
        vle = hex2int(buf[i]) / 10.0

        # if vle < 100:
        #     vle = 0

        temp_x = math.cos(angle) * vle
        temp_y = math.sin(angle) * vle
        if temp_x < -1600:
            temp_x = -1600
        elif temp_x > 1600:
            temp_x = 1600
        temp_x = int(temp_x)
        if temp_y < 0:
            temp_y = 0
        elif temp_y > 800:
            temp_y = 800
        temp_y = int(temp_y)

        xdata.append(temp_x)
        ydata.append(temp_y)
        for lane_index in range(0, 6):
            if temp_x >= AllConfig.lane_min[lane_index] and temp_x <= AllConfig.lane_max[lane_index]:
                # if temp_y > 50 and temp_y < height[lane_index]:
                if temp_y < height[lane_index]:
                    height[lane_index] = temp_y
        
    analysis_list = ['null']*6 
    for lane_index in range(0, 6):
        analysis_list[lane_index] = car_info[lane_index].insert_frame_info(height[lane_index])
    return xdata, ydata, height, analysis_list


def read_frame(ar, queue, web_frame_queue, car_queue):
    """
    读取处理每一帧雷达原始数据的信息
    """

    car_info = [None]*6
    for index in range(0, 6):
        car_info[index] = CarInfo(index)
    '''
    car_info[0].horizon_line = 559
    car_info[1].horizon_line = 371
    car_info[2].horizon_line = 563
    car_info[3].horizon_line = 605
    car_info[4].horizon_line = 502
    car_info[5].horizon_line = 650
    '''
    car_info[0].horizon_line = AllConfig.lane_horizon[0]
    car_info[1].horizon_line = AllConfig.lane_horizon[1]
    car_info[2].horizon_line = AllConfig.lane_horizon[2]
    car_info[3].horizon_line = AllConfig.lane_horizon[3]
    car_info[4].horizon_line = AllConfig.lane_horizon[4]
    car_info[5].horizon_line = AllConfig.lane_horizon[5]
    print 'car_info0.horizon_line', car_info[0].horizon_line

    # file_handle = FileHandle()

    frame_cnt = 0
    begin_flag = 'sSN'
    end_flag = '0'

    while True:
        if ar[0] == 0:
            print 'read_frame close'
            return
        # print 'read_frame process'

        while not queue.empty():
            if ar[0] == 0:
                print 'read_frame close'
                return

            if queue.qsize < 2:
                time.sleep(0.1)
                continue

            buf = queue.get()
            # print buf
            buf_split = buf.split()

            if len(buf_split) == 0:
                continue
            if buf_split[0] == begin_flag:
                if buf_split[-1] != end_flag:
                    next_buf_split = queue.get().split()
                    if len(next_buf_split) and next_buf_split[-1] == end_flag:
                        buf_split += next_buf_split
            else:
                continue
            # print buf_split

            xdata, ydata, height, analysis_data = get_frame_info(buf_split, car_info)
            '''
            for i in range(0, len(xdata)):
                print xdata[i], ydata[i]
            print ''
            print height
            '''
            for temp in analysis_data:
                if temp != 'null':
                    car_queue.put(temp)

            if web_frame_queue.empty():
                web_frame_queue.put([xdata, ydata, height, analysis_data])

        time.sleep(0.1)


def unittest(args):
    """
    单元测试
    """
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(unittest(sys.argv))
