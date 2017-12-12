#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from flask import Flask, request, jsonify 
from flask_cors import CORS
from multiprocessing import Process, Array
import read_txt
from read_txt import frame_queue, read_frame
import json

app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False 
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

'''
@app.route('/upload', methods=['GET'])
def upload():
    return jsonify({'code': 20000, 'data': 'hello'})
'''
info_list = []
@app.route('/upload', methods=['POST'])
def upload():
    global info_list
    # print(request.get_data().decode('utf-8'))
    print(json.loads(request.form['data']))
    info_list += json.loads(request.form['data'])
    return jsonify({'code': 20000, 'data': 'hello'})

@app.route('/info', methods=['GET'])
def info():
    global info_list
    # print(request.get_data().decode('utf-8'))
    # return json.dumps(info_list, ensure_ascii=False)
    return jsonify(info_list)

def init():
    frame_process = Process(target=read_txt.read)
    frame_process.start()

if __name__ == '__main__':
    # init()
    app.run(debug=True, host="0.0.0.0", port=2222)
