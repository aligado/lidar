# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask, request, jsonify, after_this_request
from flask_cors import CORS
from cStringIO import StringIO as IO
import json
import gzip
import functools 
from lidar import LidarHandle
from mtools import hexstr2int, queue, AllConfig
from multiprocessing import Process, Array, Value, Queue
import time
from frame import read_frame
from analysis import car_analysis

app = Flask(__name__)
CORS(app)

def gzipped(f):
    @functools.wraps(f)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response):
            accept_encoding = request.headers.get('Accept-Encoding', '')

            if 'gzip' not in accept_encoding.lower():
                return response

            response.direct_passthrough = False

            if (response.status_code < 200 or
                response.status_code >= 300 or 
                'Content-Encoding' in response.headers):
                return response
            gzip_buffer = IO()
            gzip_file = gzip.GzipFile(mode='wb', 
                                      fileobj=gzip_buffer)
            gzip_file.write(response.data)
            gzip_file.close()

            response.data = gzip_buffer.getvalue()
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Vary'] = 'Accept-Encoding'
            response.headers['Content-Length'] = len(response.data)

            return response

        return f(*args, **kwargs)

    return view_func

@app.route('/frame', methods=['GET'])
@gzipped
def frame():
    '''
    Handle.web_frame_queue.clear()
    while Handle.web_frame_queue.qsize() == 0:
        time.sleep(0.1) 
    '''
    temp = Handle.web_frame_queue.get()
    res = {
        'x': temp[0],
        'y': temp[1],
        'height': temp[2],
        'analysis': temp[3]
    }
    return jsonify({'data': res,
                    'code': 20000})

@app.route('/info', methods=['GET'])
@gzipped
def info():
    res = {
        'hello': [[123, 643, 789, 1243, 1234, 6666]]*3000
    }
    return jsonify(res)

@app.route('/poweron', methods=['GET'])
def poweron():
    res = {
        'code': 20000,
        'data': 'ok'
    }
    system_poweron()
    return jsonify(res)

@app.route('/car', methods=['GET'])
def car():
    cnt = 0
    data = []
    while (not Handle.web_car_queue.empty()) and (cnt <10):
        data.append(Handle.web_car_queue.get())
        cnt += 1
    res = {
        'code': 20000,
        'data': data 
    }
    return jsonify(res)

@app.route('/shutdown', methods=['GET'])
def shutdown():
    res = {
        'code': 20000,
        'data': 'ok'
    }
    system_shutdown()
    return jsonify(res)

'''
@app.route('/config', methods=['GET'])
def config():
    fp = open('lidarconfig.json', 'r+')
    content = json.loads(fp.read())
    fp.close()
    res = {
        'hello': 'world'
    }
    return jsonify(content)
'''

@app.route('/config', methods=['GET'])
def config():
    fp = open('lidarconfig.json', 'r+')
    content = json.loads(fp.read())
    fp.close()
    res = {
        'hello': 'world'
    }
    return jsonify(content)

class Handle(object):
    lidar = None
    scan_flag = Array('i', 5)
    scandata1_process = None
    read_process = None
    car_process = None
    frame_queue = queue
    web_frame_queue = Queue()
    web_lane_queue = Queue()
    web_car_queue = Queue()
    car_queue = Queue()
    
    @classmethod
    def create_scan_process(cls):
        cls.scan_flag[0] = 1
        cls.scandata1_process = Process(target=cls.lidar.open_scandata1,
                                        args=(cls.scan_flag, ))
        cls.scandata1_process.daemon = True
        cls.scandata1_process.start()
    
    @classmethod
    def create_read_process(cls):
        cls.read_process = Process(target=read_frame,
                                   args=(cls.scan_flag,
                                         cls.frame_queue,
                                         cls.web_frame_queue,
                                         cls.car_queue))
        cls.read_process.daemon = True
        cls.read_process.start()

    @classmethod
    def create_analysis_process(cls):
        cls.car_process = Process(target=car_analysis,
                                  args=(cls.scan_flag,
                                        cls.car_queue,
                                        cls.web_car_queue))
        cls.car_process.daemon = True
        cls.car_process.start()

    @classmethod
    def connect(cls):
        cls.lidar = LidarHandle(AllConfig.host, AllConfig.port)
        cls.lidar.connect()

    @classmethod
    def close_scan_process(cls):
        cls.lidar.close_scandata1(cls.scan_flag)

    @classmethod
    def close_lidar(cls):
        cls.lidar.close()

def system_shutdown():
    # time.sleep(600)
    Handle.close_scan_process()
    print 'close_scan_process'
    time.sleep(3)
    Handle.close_lidar()
    print 'close_lidar'
     
def system_poweron():
    """
    初始化
    """
    AllConfig.read_config_file()
    Handle.connect()
    Handle.create_scan_process()
    print 'create_scan_process'
    Handle.create_read_process()
    print 'create_read_process'
    Handle.create_analysis_process()
    print 'create_analysis_process'
    '''
    while not Handle.frame_queue.empty():
        print Handle.frame_queue.get()
        print ""
    '''
    time.sleep(3)

if __name__ == '__main__':
    # system_poweron()
    app.run(debug=True, host="0.0.0.0", port=8080)
