# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: alpc32
# Date: 2017-09-12 22:29:40
# Last Modified by:   alpc32
# Last Modified time: Wed Jun  6 23:05:28 CST 2018
 
import time
import math
from util import DataBuf, hexstr2int, AllConfig
try:
    import cv2
    import numpy as np
except Exception as identifier:
    cv2 = None
    print('arm platform')

PI = math.pi
hex2int = hexstr2int

HIGHT_TABLE = {}

class CarInfo(object):
    """
    frameinfo object
    收集车道上经过每辆车雷达点阵信息
    """

    def __init__(self, id):
        self.height_list = []  # 车辆波形数组
        self.width_list = []  # 车辆波形数组
        self.horizon_line = 0  # 车道水平线,修正高度
        self.under_cnt = 0  # 连续空白无车辆计数
        self.id = id  # 车道id
        self.threshold_num = AllConfig.threshold_num  # 连续点阈值
        self.threshold_height = AllConfig.threshold_height  # 高度阈值
        # print 'threshold', self.threshold_num, self.threshold_height

    def insert_frame_info(self, height, width=0):
        """
        插入单侦车辆高度信息
        """

        # 由于雷达倒装
        # 车的高度等于标定水平线减去
        height = self.horizon_line - height
        if height < 0:
            height = 0

        self.height_list.append(height)
        self.width_list.append(width)

        # print(height)
        # 如果扫描点连续threshold_num个低于threshold_height
        # 则断开info_list为一个车辆的数据
        if height < self.threshold_height:
            self.under_cnt += 1
            if self.under_cnt >= self.threshold_num:
                res = self.car_analysis()
                self.height_list = []
                self.width_list = []
                self.under_cnt = 0
        else:
            self.under_cnt = 0

    def car_analysis(self):
        """
        将info_list去头截尾得到
        一个车辆完整的高度轮廓
        """
        # print('id info_list', self.id, info_list)
        info_list = self.height_list
        info_len = len(info_list)
        begin = 0
        end = info_len - self.threshold_num
        while begin < info_len and info_list[begin] < self.threshold_height:
            begin += 1
        # print('begin end', begin, end)
        if begin+self.threshold_num < end:
            height_list = self.height_list[begin:end]
            width_list = self.width_list[begin:end]
            
            # info_len = len(info_list)
            if len(height_list) > 4:
                print 'car height list:', height_list
                DataBuf.car.put({
                    'id': self.id,
                    'info_list': height_list,
                    'width_list': width_list
                })

def get_frame_info(buf, car_info):

    """
    @buf 雷达split之后的侦数据
    @car_info  单个车辆的雷数信息
    将帧的信息分为6个车道进行处理
    """
    def cv_draw(xdata, ydata):
        image_content = np.zeros((400, 1280, 3), np.uint8)
        # print('frame_draw')
        image_content[0:0+5, 640:640+2] = (0, 255, 255)

        for index, h in enumerate(AllConfig.lane):
            lane_min = AllConfig.lane[index][0] + 2000
            lane_max = AllConfig.lane[index][1] + 2000
            x1 = 1280*lane_min/4000
            x2 = 1280*lane_max/4000
            y = 400*(AllConfig.lane[index][2])/1000
            image_content[y-10:y+10, x1-1:x1+1] = (255, 255, 0)
            image_content[y-10:y+10, x2-1:x2+1] = (255, 255, 0)
            image_content[y:y+1, x1:x2+1] = (255, 255, 0)

        for point_y1 in range(0, 800, 100):
            point_y2 = point_y1+100

            y1 = 400*point_y1/1000
            y2 = 400*point_y2/1000
            x1 = 640
            x2 = 640

            image_content[y1:y1+2, x1:x1+10] = (255, 0, 0)
            image_content[y2:y2+2, x2:x2+10] = (255, 0, 0)
            image_content[y1:y2+1, x1:x1+1] = (255, 0, 0)

            cv2.putText(image_content, str(point_y1), (x1+10, y1),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 255),
                        1)

        for point_x1 in range(-1600, 1600, 100):
            point_x2 = point_x1+100

            lane_min = point_x1 + 2000
            lane_max = point_x2 + 2000

            x1 = 1280*lane_min/4000
            x2 = 1280*lane_max/4000

            y = 400*700/1000
            image_content[y-10:y+10, x1-1:x1+1] = (255, 0, 0)
            image_content[y-10:y+10, x2-1:x2+1] = (255, 0, 0)
            image_content[y:y+1, x1:x2+1] = (255, 0, 0)

            cv2.putText(image_content, str(point_x1), (x1-10, y+20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 255),
                        1)
        
        for key, value in HIGHT_TABLE.items():
            x1 = key + 2000
            x1 = 1280*x1/4000
            y = 400*700/1000
            image_content[y:y+value, x1:x1+1] = (255, 255, 0)


        for index, x in enumerate(xdata):
            y = ydata[index]
            x += 2000
            x = 1280*x/4000
            y = 400*y/1000
            image_content[y:y+1, x:x+1] = (0, 0, 255)
        cv2.imshow('cvdraw', image_content)
        k = cv2.waitKey(20)

    xdata, ydata = [], []  # 单侦雷达数据的二维点阵
    buf_len = len(buf)

    if buf_len < 26:
        return

    # 雷达扫描点数
    num_len = hex2int(buf[25])
    end = min(26+num_len, buf_len)

    lane_num = len(AllConfig.lane)
    height = [6666]*lane_num
    width = [0]*lane_num
    x_range = [[], [], [], [], [], []]

    lidar_fix_angle = AllConfig.lidar_fix_angle

    MINI_Y = 30
    CAR_H = 150
    CAR_RANGE_H = 20
    
    for i in range(26, end):
        angle = ((i - 26 + lidar_fix_angle) * 0.5 + 0) * PI / 180.0
        vle = hex2int(buf[i]) / 10.0

        temp_x = math.cos(angle) * vle
        temp_y = math.sin(angle) * vle

        temp_y = int(temp_y)
        temp_x = int(temp_x)

        # 添加二维点
        xdata.append(temp_x)
        ydata.append(temp_y)
        
        # 遍历6个车道，找到每个车道最高点
        for lane_index in range(0, lane_num):
            [minx, maxx, horizon] = AllConfig.lane[lane_index]
            if (temp_x >= AllConfig.lane[lane_index][0] and
                temp_x <= AllConfig.lane[lane_index][1]):
                if temp_y > MINI_Y:

                    if cv2:
                        if AllConfig.lane[lane_index][2] - temp_y > CAR_H:
                            if temp_x in HIGHT_TABLE:
                                HIGHT_TABLE[temp_x] += 1
                            else:
                                HIGHT_TABLE[temp_x] = 1

                    if AllConfig.lane[lane_index][2] - temp_y > CAR_RANGE_H:
                        x_range[lane_index].append(temp_x)

                    if temp_y < height[lane_index]:
                        height[lane_index] = temp_y

    if cv2:
        cv_draw(xdata, ydata)

    for lane_index in range(0, lane_num):
        if x_range[lane_index]:
            x_range[lane_index].sort()
            width[lane_index] = x_range[lane_index][-1] - x_range[lane_index][0]
        else:
            width[lane_index] = 0

    for lane_index in range(0, 6):
        car_info[lane_index].insert_frame_info(height[lane_index],
                                               width[lane_index])

def frame_handle():
    """
    读取处理每一帧雷达原始数据的信息
    @ar [0]进程正常运行标志
    @queue 雷达原始侦数据
    @web_frame_queue web前端显示的雷达侦数据
    @car_queue 雷达扫描到的车辆高度图像信息
    """

    # 各车道车辆信息实例初始化
    lane_num = len(AllConfig.lane)
    car_info = []
    for index in range(0, lane_num):
        car_info.append(CarInfo(index))
        # 赋值各车道修正高度
        car_info[index].horizon_line = AllConfig.lane[index][2]

    # print 'car_info0.horizon_line', car_info[0].horizon_line

    begin_flag = 'sSN'  # frame begin flag
    end_flag = '0'  # frame end flag
    while True:

        queue = DataBuf.frame
        while not queue.empty():
            if DataBuf.flag[0] == 0:  # 关闭雷达侦处理进程
                print 'frame handle process close'
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
            get_frame_info(buf_split, car_info)
            '''
            xdata, ydata, height, analysis_data = get_frame_info(buf_split, car_info)
            for temp in analysis_data:
                if temp != 'null':
                    car_queue.put(temp)
            '''

        time.sleep(0.1)
    
def unittest(args):
    """
    单元测试
    """
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(unittest(sys.argv))
