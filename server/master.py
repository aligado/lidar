#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from flask import Flask, request, jsonify 
from flask_cors import CORS
from multiprocessing import Process, Array
import read_txt
from read_txt import frame_queue, read_frame

app = Flask(__name__)
CORS(app)

@app.route('/list', methods=['GET'])
def list():
    data = read_frame()
    '''
    if not frame_queue.empty():
        data = frame_queue.get()
    '''
    #print data
    print(data['height'])
    return jsonify({'code': 20000, 'data': data})

def init():
    frame_process = Process(target=read_txt.read)
    frame_process.start()

if __name__ == '__main__':
    # init()
    app.run(debug=True, host="0.0.0.0", port=2222)
