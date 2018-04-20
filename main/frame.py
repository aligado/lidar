# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: alpc32
# Date: 2017-09-12 22:29:40
# Last Modified by:   alpc32
# Last Modified time: 2018年 2月16日 星期五 16时23分27秒 CST


import time
import math
# from file_handle import FileHandle
from mtools import hexstr2int, AllConfig
import numpy as np
import cv2

PI = math.pi
hex2int = hexstr2int


class CarInfo(object):
    """
    frameinfo object
    收集车道上经过每辆车雷达点阵信息
    """
    threshold_num = AllConfig.threshold_num  # 连续点阈值
    threshold_height = AllConfig.threshold_height  # 高度阈值

    def __init__(self, id):
        self.info_list = []  # 车辆波形数组
        self.horizon_line = 0  # 车道水平线,修正高度
        self.under_cnt = 0  # 连续空白无车辆计数
        self.id = id  # 车道id

    def insert_frame_info(self, height, width=0):
        """
        插入单侦车辆高度信息
        """
        # 由于雷达倒装
        # 车的高度等于标定水平线减去
        height = self.horizon_line - height
        self.info_list.append(height)
        '''
        print('insert', height)
        print('insert', self.info_list)
        '''
        # print(height)
        # 如果扫描点连续threshold_num个低于threshold_height
        # 则断开info_list为一个车辆的数据
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
        """
        将info_list去头截尾得到
        一个车辆完整的高度轮廓
        """
        # print('id info_list', self.id, info_list)
        info_len = len(info_list)
        begin = 0
        end = info_len - self.threshold_num
        while begin < info_len and info_list[begin] < self.threshold_height:
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
    @buf 雷达split之后的侦数据
    @car_info  单个车辆的雷数信息
    将帧的信息分为6个车道进行处理
    """
    def cv_draw(xdata, ydata):
        image_content = np.zeros((720, 1280, 3), np.uint8)
        print('frame_draw')
        for index, h in enumerate(AllConfig.lane_horizon):
            lane_min = AllConfig.lane_min[index] + 2000
            lane_max = AllConfig.lane_max[index] + 2000
            x1 = 1280*lane_min/4000
            x2 = 1280*lane_max/4000
            y = 720*(AllConfig.lane_horizon[index]+100)/2000
            image_content[ y-10:y+10, x1-1:x1+1 ] = (255, 255, 0)
            image_content[ y-10:y+10, x2-1:x2+1 ] = (255, 255, 0)
            image_content[ y:y+1, x1:x2+1 ] = (255, 255, 0)

        for index, x in enumerate(xdata):
            y = ydata[index]
            x += 2000
            y += 100
            x = 1280*x/4000
            y = 720*y/2000
            image_content[ y:y+1, x:x+1] = (0, 0, 255)
        cv2.imshow('cvdraw', image_content)
        k = cv2.waitKey(20)

    xdata, ydata = [], []  # 单侦雷达数据的二维点阵
    buf_len = len(buf)

    if buf_len < 26:
        return [], [], [], []

    # 雷达扫描点数
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
        if temp_x < -2000:
            temp_x = -2000
        elif temp_x > 2000:
            temp_x = 2000
        temp_x = int(temp_x)
        if temp_y < 0:
            temp_y = 0
        elif temp_y > 1000:
            temp_y = 1000
        temp_y = int(temp_y)

        # 添加二维点
        xdata.append(temp_x)
        ydata.append(temp_y)


        # 遍历6个车道，找到每个车道最高点
        for lane_index in range(0, 6):
            if temp_x >= AllConfig.lane_min[lane_index] and temp_x <= AllConfig.lane_max[lane_index]:
                # if temp_y > 50 and temp_y < height[lane_index]:
                if temp_y < height[lane_index]:
                    height[lane_index] = temp_y

    cv_draw(xdata, ydata)

    analysis_list = ['null']*6
    for lane_index in range(0, 6):
        analysis_list[lane_index] = car_info[lane_index].insert_frame_info(height[lane_index])
    return xdata, ydata, height, analysis_list


def read_frame(ar, queue, web_frame_queue, car_queue):
    """
    读取处理每一帧雷达原始数据的信息
    @ar [0]进程正常运行标志
    @queue 雷达原始侦数据
    @web_frame_queue web前端显示的雷达侦数据
    @car_queue 雷达扫描到的车辆高度图像信息
    """

    # 各车道车辆信息实例初始化
    car_info = [None]*6  # need update
    for index in range(0, 6):
        car_info[index] = CarInfo(index)
    # 赋值各车道修正高度
    car_info[0].horizon_line = AllConfig.lane_horizon[0]
    car_info[1].horizon_line = AllConfig.lane_horizon[1]
    car_info[2].horizon_line = AllConfig.lane_horizon[2]
    car_info[3].horizon_line = AllConfig.lane_horizon[3]
    car_info[4].horizon_line = AllConfig.lane_horizon[4]
    car_info[5].horizon_line = AllConfig.lane_horizon[5]
    # for debug
    print 'car_info0.horizon_line', car_info[0].horizon_line

    # frame_cnt = 0
    begin_flag = 'sSN'  # frame begin flag
    end_flag = '0'  # frame end flag

    while True:
        if ar[0] == 0:  # 关闭雷达侦处理进程
            print 'read_frame close'
            return

        while not queue.empty():
            if ar[0] == 0:  # 关闭雷达侦处理进程
                print 'read_frame close'
                return

            # 必须至少要有两侦的数据才去处理
            # 解决侦不全的情况
            if queue.qsize < 2:
                time.sleep(0.1)
                continue

            buf = queue.get()
            # print buf
            buf_split = buf.split()

            if len(buf_split) == 0:  # 无意义侦跳过
                continue
            # 处理尾部不完整的侦
            if buf_split[0] == begin_flag:
                if buf_split[-1] != end_flag:
                    next_buf_split = queue.get().split()
                    if len(next_buf_split) and next_buf_split[-1] == end_flag:
                        buf_split += next_buf_split
            else:
                continue
            # print buf_split

            # 将侦数据交由下一层函数处理
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
