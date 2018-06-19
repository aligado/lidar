# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: alpc32
# Date: 2017-09-12 22:29:40
# Last Modified by:   alpc32
# Last Modified time: 2017-09-12 22:29:40

import time
import math
from util import DataBuf, hexstr2int, AllConfig, PI
import json

try:
    import cv2
    import numpy as np
except Exception as identifier:
    cv2 = None
    print('arm platform')


class FileHandle(object):
    def __init__(self):
        self.file_tips = self.get_tips()
        self.file_write_cnt = 0
        self.max_cnt = 5
        self.file_buf = ""
        self.path = 'out/'
    
    @classmethod
    def parse_mess(cls, json_data):
        def temp_mess():
            temp = {
                'num': [0]*9,
                'spd': [32]*9
            }
            return temp
        res = []
        for index in range(0, 6):
            res.append(temp_mess())

        for car_data in json_data:
            lane_id = car_data['lane_id']
            if 'type' in car_data:
                res[lane_id]['num'][car_data['type']] += 1
            else:
                res[lane_id]['num'][0] += 1
        print res
        return res

    def record(self, buf):
        self.file_write_cnt += 1
        if self.file_buf == "":
            self.file_buf = []
        self.file_buf.append(buf)
        print '[record]', buf, self.file_write_cnt
        if self.file_write_cnt >= self.max_cnt:
            self.file_write_cnt = 0
            now_tips = self.get_tips()
            if now_tips != self.file_tips and self.suit_tips(now_tips):
                fp = open(self.path + now_tips + '.json', 'w+')
                fp.write(json.dumps(self.file_buf))
                fp.close()
                temp = self.parse_mess(self.file_buf)
                print temp

                # send_msg(temp)
                DataBuf.res.put(temp)
                self.file_buf = ""
                self.file_tips = now_tips
    
    @staticmethod
    def get_tips():
        return time.strftime('%Y%m%d%H%M')

    @staticmethod
    def suit_tips(tips):
        return tips[-1] == '0' or tips[-1] == '5'
        return True
        # return int(tips[-1]) % 2 == 0

def car_analysis():
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
        image_content[0:720, 0:1280] = (255, 255, 255)
        print('car_draw')
        step = 30
        for index, y in enumerate(info_list):
            x = step*index+2
            y = 720 - y*2
            image_content[ y:y+5, x:x+5] = (0, 0, 255)
        cv2.imshow('cvcar', image_content)
        k = cv2.waitKey(20)

    while True:
        if DataBuf.flag[0] == 0:
            print 'close car analysis'
            return
        # print 'car_analysis'
        while not DataBuf.car.empty():
            # print 'car_analysis'
            temp = DataBuf.car.get()
            print 'car info', temp
            info_list = temp['info_list']
            lane_id = temp['id']
            car_res = {
                'lane_id': lane_id,
                'height_list': info_list,
                'width_list': temp['width_list']
            }
            car_type = use_model(car_res)
            car_res['type'] = car_type
            if cv2:
                cv_draw(info_list)
            print 'car_res', car_res
            car_file.record(car_res)
            # web_car_queue.put(car_res)
        time.sleep(0.1)

def use_model(car_res):
    return 0

'''
def use_model(car_res):
    car_model = [
        {
            'name': 'car', # 小客
            'average_height': [100, 180],
            'length': [5, 10]
        },
        {
            'name': 'small lorry', # 小货
            'average_height': [200, 300],
            'length': [10, 20]
        },
        {
            'name': 'bus', # 大客
            'average_height': [181, 300],
            'avarage_q': [0, 60],
            'length': [8, 12]
        },
        {
            'name': 'lorry', # 中货
            'average_height': [200, 250],
            'length': [5, 10]
        },
        {
            'name': 'truck', # 大货
            'average_height': [250, 300],
            'length': [10, 20]
        },
        {
            'name': 'huge truck', # 特大货 
            'average_height': [300, 380],
            'length': [20, 200]
        },
        {
            'name': 'trailer', # 拖挂车 集装箱
            'average_height': [380, 600],
            'length': [24, 300]
        },
        {
            'name': 'motor', # 摩托
            'average_height': [100, 150],
            'length': [2, 5]
        }
    ]
    for key, model in enumerate(car_model):
        if (car_res['average_height'] >= model['average_height'][0] and
            car_res['average_height'] <= model['average_height'][1] and
            car_res['revolution'] >= model['length'][0] and
            car_res['revolution'] <= model['length'][1]):
            if 'average_q' in model:
                if (car_res['average_q'] >= model['average_q'][0] and
                    car_res['average_q'] <= model['average_q'][1]):
                    return key
            else:
                return key
    return 0
'''