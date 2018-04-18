#! usr/bin/python
# coding=utf-8 
import socket
import json
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
#s.connect(('127.0.0.1', 9999))
s.connect(('119.29.186.141', 8006))
print s.recv(1024)
data = "LMDscandata"
s.send(data)
print s.recv(1024)
s.close()