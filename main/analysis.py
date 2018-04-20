# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: alpc32
# Date: 2017-09-12 22:29:40
# Last Modified by:   alpc32
# Last Modified time: 2017-09-12 22:29:40

import time
import math
from file_handle import FileHandle
from mtools import queue, hexstr2int, AllConfig, PI
import json
import cv2
import numpy as np


def car_analysis(ar, car_queue, web_car_queue):
    """
    @ar 进程共享变量控制进程开关
    @car_queue 车辆信息队列
    @web_car_queue 前端可视的探测车辆信息
    车辆分析主程
    car_queue存储所有探测到车辆的雷达波形
    能够解析到的信息包括
    车辆平均高度,方差,波形长度,车道id
    """
    car_file = FileHandle()

    def cv_draw(info_list):
        image_content = np.zeros((720, 1280, 3), np.uint8)
        print('car_draw')
        step = 30
        for index, y in enumerate(info_list):
            x = step*index+2
            y = 720 - y*2
            image_content[ y:y+1, x:x+1] = (0, 0, 255)
        cv2.imshow('cvcar', image_content)
        k = cv2.waitKey(20)

    while True:
        if ar[0] == 0:
            print 'close car analysis'
            return
        # print 'car_analysis'
        while not car_queue.empty():
            if ar[0] == 0:
                print 'close car analysis'
                return
            # print 'car_analysis'
            temp = car_queue.get()
            print 'car info', temp
            info_list = temp['info_list']
            lane_id = temp['id']
            info_len = len(info_list)
            average_height = 0
            max_height = 0
            for height in info_list:
                average_height += height
                max_height = max(max_height, height)
            average_height /= info_len

            average_q = 0
            for height in info_list:
                average_q += (height-average_height)*(height-average_height)
            average_q = int(math.sqrt(average_q))

            '''
            print'average_height', average_height
            print'average_q', average_q
            print'analysis_list', info_list
            print'revolution', info_len
            print'lane id', lane_id
            '''
            car_res = {
                'info_list': info_list,
                'average_height': average_height,
                'revolution': info_len,
                'lane id': lane_id,
                'max_height': max_height,
                'average_q': average_q
            }
            cv_draw(info_list)
            '''
            print 'web_car_queue', web_car_queue.qsize()
            if web_car_queue.qsize < 5000:
                web_car_queue.put(car_res)
                print 'insert car'
            '''
            print 'car_res', car_res
            car_file.write_json(car_res)
            # web_car_queue.put(car_res)
        time.sleep(0.1)


if __name__ == '__main__':
    # import sys
    pass
