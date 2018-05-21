#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from datetime import datetime
import json
from proxy import send_msg 
import threading

class FileHandle(object):
    def __init__(self):
        self.file_tips = self.get_tips()
        self.file_write_cnt = 0
        self.max_cnt = 5
        self.file_buf = ""
        self.path = 'out/'
    
    @classmethod
    def parse_mess(cls, json_data):
        res = [
            {
                'total': [0]*9
            },
            {
                'total': [0]*9
            },
            {
                'total': [0]*9
            },
            {
                'total': [0]*9
            },
            {
                'total': [0]*9
            },
            {
                'total': [0]*9
            }
        ]
        for car_data in json_data:
            lane_id = car_data['lane_id']
            if 'type' in car_data:
                res[lane_id]['total'][car_data['type']] += 1
            else:
                res[lane_id]['total'][0] += 1
        print res
        return res

    def write_json(self, buf, res_queue):
        self.file_write_cnt += 1
        if self.file_buf == "":
            self.file_buf = []
        self.file_buf.append(buf)
        print 'write_json', buf, self.file_write_cnt
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
                res_queue.put(temp)
                '''
                send_msg_thread = threading.Thread(target=send_msg,
                                                   args=(temp, ))
                send_msg_thread.daemon = True
                send_msg_thread.start()
                '''

                self.file_buf = ""
                self.file_tips = now_tips
    
    @staticmethod
    def get_tips():
        return time.strftime('%Y%m%d%H%M')

    @staticmethod
    def suit_tips(tips):
        # return True
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
