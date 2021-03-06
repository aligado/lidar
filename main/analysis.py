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


def car_analysis(ar, car_queue, web_car_queue):
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
            web_car_queue.put(car_res)
            print car_res
        time.sleep(0.1)

if __name__ == '__main__':
    import sys
    sys.exit(unittest(sys.argv))
