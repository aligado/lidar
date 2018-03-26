#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from datetime import datetime
import json

class FileHandle(object):
    def __init__(self):
        self.file_tips = self.get_tips()
        self.file_write_cnt = 0
        self.max_cnt = 5
        self.file_buf = ""
        self.path = 'out/'

    def write_json(self, buf):
        self.file_write_cnt += 1
        if self.file_buf == "":
            self.file_buf = []
        self.file_buf.append(buf)
        print buf, self.file_write_cnt
        if self.file_write_cnt >= self.max_cnt:
            self.file_write_cnt = 0
            now_tips = self.get_tips()
            if now_tips != self.file_tips and self.suit_tips(now_tips):
                fp = open(self.path + now_tips + '.json', 'w+')
                fp.write(json.dumps(self.file_buf))
                fp.close()
                self.file_buf = "" 
                self.file_tips = now_tips

    def write_buf(self, buf):
        self.file_write_cnt += 1
        self.file_buf += buf + '\n'
        print buf, self.file_write_cnt
        if self.file_write_cnt >= self.max_cnt:
            self.file_write_cnt = 0
            now_tips = self.get_tips()
            if now_tips != self.file_tips and self.suit_tips(now_tips):
                fp = open(self.path + now_tips + '.txt', 'w+')
                fp.write(self.file_buf)
                fp.close()
                self.file_buf = ''
                self.file_tips = now_tips
    
    def tcp_client(self, buf):
        pass

    @staticmethod
    def get_tips():
        return time.strftime('%Y%m%d%H%M')

    @staticmethod
    def suit_tips(tips):
        return tips[-1] == '0' or tips[-1] == '5'
        # return int(tips[-1]) % 2 == 0


def test(argv):
    test_file_handle = FileHandle()
    cnt = 0
    while True:
        cnt += 1
        print cnt
        test_file_handle.write(str(cnt) + '\n')
        time.sleep(1)
        if cnt == 700:
            break


if __name__ == '__main__':
    import sys
    sys.exit(test(sys.argv))
