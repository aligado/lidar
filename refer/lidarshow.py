#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  lidarshow.py
#  
#  Copyright 2017 alpc32 <alpc32@ALPC>

import socket
import time
from ctypes import c_int32
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
	xdata, ydata = [], []
	temp_ss = buf.split()
	print temp_ss
	len = hex2int(temp_ss[25])
	print 'len ', len
	for i in range(26, 26+len):
		#print i-25,' ',temp_ss[i]
		angle = ((i-26)*Conf.resolution + 0)*3.1415926 / 180
		vle = hex2int(temp_ss[i])/1000.0
		xdata.append( np.cos(angle)*vle )
		ydata.append( np.sin(angle)*vle )
	return xdata, ydata
		
s.connect(('192.168.0.2', 2111))
s.send("sRN LMPscancfg")
buf = s.recv(2048)
process_buf(buf)
process_conf(buf)    

'''
cnt = 1
while cnt:
    s.send("sRN LMDscandata")
    buf = s.recv(2048)
    process_buf(buf)
    process_data(buf)
    cnt -= 1
'''
# 接收数据:

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r', animated=True)
#plt.xlim(-10, 10)
#plt.ylim(-10, 10)

def init():
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    return ln,

def update(frame):
    #xdata.append(frame)  
    #ydata.append(np.sin(frame))
    s.send("sRN LMDscandata")
    buf = s.recv(3072)
    if len(buf)<100:
		return ln,
    ln.set_data(process_data(buf))
    return ln,

ani = FuncAnimation(fig, update, interval=100, init_func=init, blit=True)
plt.show()

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
