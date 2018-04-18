# -*- coding: utf-8 -*-
"""
"""

import socket
import time
from ctypes import c_int32
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

class Conf:
	frequency = 0
	resolution = 0
	start_angle = 0
	stop_angle = 0
	
def process_buf(buf):
    print buf
    temp_ss = buf.split()
    print 'len',len(buf),'num',len(temp_ss)
    print temp_ss
    #time.sleep(2)

def hex2int(hex_int):
	return c_int32(int(hex_int, 16)).value

def process_conf(buf):
	temp_ss = buf.split()
	Conf.frequency = hex2int(temp_ss[2])/100
	Conf.resolution = hex2int(temp_ss[4])*1.0/10000.0
	Conf.start_angle = hex2int(temp_ss[5])*1.0/10000.0
	Conf.stop_angle = hex2int(temp_ss[6][0:-1])*1.0/10000.0
	print Conf.__dict__
	#print Conf

def process_data(buf):
	data = []
	temp_ss = buf.split()
	len = hex2int(temp_ss[25])
	print 'len ', len
	for i in range(26, 26+len):
		print i-25,' ',temp_ss[i]
		
s.connect(('192.168.0.2', 2111))
s.send("sRN LMPscancfg")
buf = s.recv(2048)
process_buf(buf)
process_conf(buf)    

cnt = 1
while cnt:
    s.send("sRN LMDscandata")
    buf = s.recv(2048)
    process_buf(buf)
    process_data(buf)
    cnt -= 1
# 接收数据:
'''
buffer = []
while True:
    # 每次最多接收1k字节:
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
data = ''.join(buffer)
print data
'''
s.close()
