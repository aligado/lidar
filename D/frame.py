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


def get_frame_info(frame):
    """
    获得每一帧的关键信息
    """

    class FrameInfo(object):
        """
        frameinfo object
        """

        def __init__(self):
            self.result = [0] * 12
            self.index = 0

        def insert_point(self, x, y):
            index = 0
            for index in range(0, AllConfig.lane_num):
                # print index
                # print AllConfig.lane_min[index], AllConfig.lane_max[index]
                if (x >= AllConfig.lane_min[index]) and (x <= AllConfig.lane_max[index]):
                    # print 'index', index
                    self.result[index * 2] = max(self.result[index * 2], y)
                    self.result[index * 2 + 1] += 1
                    break
        '''
        def insert_point(self, x, y):
            if x < AllConfig.lane_min[self.index]:
                return True
            while self.index < AllConfig.lane_num and x > AllConfig.lane_max[self.index]:
                self.index += 1
            if self.index == AllConfig.lane_num:
                return False
            print 'index', self.index
            self.result[self.index * 2] = max(self.result[self.index * 2], y)
            self.result[self.index * 2 + 1] += 1
        '''

    i = 0
    frame_info = FrameInfo()
    temp_pi = PI / 180.0
    for value in frame:
        angle = (i * AllConfig.lidar_resolution + 0) * temp_pi
        i += 1
        vle = hexstr2int(value) / 10.0
        temp_x = int(math.cos(angle) * vle)
        temp_y = int(AllConfig.lidar_height - math.sin(angle) * vle)
        if temp_y < AllConfig.car_threshold:
            continue

        # print "insert point", temp_x, temp_y
        frame_info.insert_point(temp_x, temp_y)

    print 'result ', frame_info.result
    frame_info_queue.put(frame_info.result)
    return ' '.join(str(temp) for temp in frame_info.result)


def process_frame(ar):
    """
    处理雷达每帧数据
    """
    # file_handle = FileHandle()
    frame_cnt = 0
    while True:
        global error_frame
        for temp_i in range(0, 6):
            print 'queuesize', queue.qsize(), 'frame_cnt', frame_cnt, 'error frame', error_frame
        # 处理queue队列中留存的所有扫描数据
        while not queue.empty():
            buf = queue.get()
            # print buf
            buf_split = buf.split()
            buf_split_len = len(buf_split)
            if buf[0] != '\x02' or buf_split_len < 26:
                error_frame += 1
                print "Erro frame"
                continue

            frame_cnt += 1
            point_num = min(hexstr2int(buf_split[25]), buf_split_len - 26)
            # print 'point_num', point_num

            # print buf_split[9], buf_split[10], process_frame(buf_split[26:26+point_num])
            result_data = buf_split[9] + ' ' + \
                get_frame_info(buf_split[26:26 + point_num])
            # result_data = process_frame(buf_split[26:26+proint_num])
            # file_handle.write(result_data + '\n')
            # return
        if ar[0] == 0:
            return
        time.sleep(0.1)


def unittest(args):
    """
    单元测试
    """
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(unittest(sys.argv))
