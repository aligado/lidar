# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: alpc32
# Date: 2017-09-12 22:29:40
# Last Modified by:   alpc32
# Last Modified time: 2017-09-12 22:29:40

import time
import math
from file_handle import FileHandle
from mtools import queue, height_queue, hexstr2int, AllConfig, PI


def get_frame_info(frame):
    """
    获得每一帧的关键信息
    """

    class FrameInfo(object):
        """
        frameinfo object
        """
        def __init__(self):
            self.result = [] * 12
            self.index = 0

        def insert_point(self, x, y):
            if x < AllConfig.lane_min[index]:
                return True
            while index < AllConfig.lane_num and x > AllConfig.lane_max[index]:
                index += 1
            if index == AllConfig.lane_num:
                return False
            self.result[index * 2] = max(self.result[index * 2], y)
            self.result[index * 2 + 1] += 1

    i = 0
    frame_info = FrameInfo()
    for value in frame:
        angle = (i * AllConfig.lidar_resolution + 0) * PI / 180
        i += 1
        vle = hexstr2int(value) / 10.0
        temp_x = int(math.cos(angle) * vle)
        temp_y = int(AllConfig.lidar_height - math.sin(angle) * vle)
        if temp_y < AllConfig.threshold:
            continue
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
        print 'queuesize', queue.qsize(), 'frame_cnt', frame_cnt
        # 处理queue队列中留存的所有扫描数据
        while not queue.empty():
            buf = queue.get()
            # print buf
            buf_split = buf.split()
            buf_split_len = len(buf_split)
            if buf[0] != '\x02' or buf_split_len < 26:
                print "Erro frame"
                continue

            frame_cnt += 1
            point_num = min(hexstr2int(buf_split[25]), buf_split_len - 26)

            # print buf_split[9], buf_split[10], process_frame(buf_split[26:26+point_num])
            result_data = buf_split[9] + ' ' + \
                get_frame_info(buf_split[26:26 + point_num])
            #result_data = process_frame(buf_split[26:26+proint_num])
            # file_handle.write(result_data + '\n')
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
