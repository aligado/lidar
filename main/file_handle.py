#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from datetime import datetime


class FileHandle(object):
    def __init__(self):
        self.temp_fp = open("temp.txt", 'w')
        self.file_tips = self.get_tips()
        self.file_write_cnt = 0
        self.file_buf = ""

    def write(self, buf):
        self.file_write_cnt += 1
        self.file_buf += buf
        self.temp_fp.write(buf)
        # print self.file_buf
        if self.file_write_cnt == 200:
            self.file_write_cnt = 0
            now_tips = self.get_tips()
            if now_tips != self.file_tips and self.suit_tips(now_tips):
                os.rename("temp.txt", now_tips + '.txt')
                '''
                file_handle = open(now_tips+'.txt', 'w+')
                file_handle.write(self.file_buf)
                file_handle.close()
                self.file_buf = ""
                '''
                self.temp_fp = open("temp.txt", 'w')
                self.file_tips = now_tips

    @staticmethod
    def get_tips():
        return time.strftime('%Y%m%d%H%M')

    @staticmethod
    def suit_tips(tips):
        return tips[-1] == '0' or tips[-1] == '5'


def test(argv):
    test_file_handle = FileHandle()
    cnt = 0
    while True:
        cnt += 1
        print cnt
        test_file_handle.write(str(cnt) + '\n')
        time.sleep(0.02)
        if cnt == 60000:
            break


if __name__ == '__main__':
    import sys
    sys.exit(test(sys.argv))
