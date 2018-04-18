# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask, request, jsonify, after_this_request
from flask_cors import CORS
from cStringIO import StringIO as IO
import json
import gzip
import functools 

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

@app.route('/info', methods=['GET'])
@gzipped
def info():
    fp = open('lidarconfig.json', 'r+')
    content = json.loads(fp.read())
    fp.close()
    res = {
        'hello': [[123, 643, 789, 1243, 1234, 6666]]*3000
    }
    return jsonify(res)

@app.route('/config', methods=['GET'])
def config():
    fp = open('lidarconfig.json', 'r+')
    content = json.loads(fp.read())
    fp.close()
    res = {
        'hello': 'world'
    }
    return jsonify(content)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
