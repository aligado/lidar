import socket
import time
from ctypes import c_int32
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Conf:
    frequency = 0
    resolution = 0
    start_angle = 0
    stop_angle = 0


def process_buf(buf):
    print buf
    temp_ss = buf.split()
    print 'len', len(buf), 'num', len(temp_ss)
    print temp_ss


# time.sleep(2)

def hex2int(hex_int):
    return c_int32(int(hex_int, 16)).value


def process_conf(buf):
    temp_ss = buf.split()
    Conf.frequency = hex2int(temp_ss[2]) / 100
    Conf.resolution = hex2int(temp_ss[4]) * 1.0 / 10000.0
    Conf.start_angle = hex2int(temp_ss[5]) * 1.0 / 10000.0
    Conf.stop_angle = hex2int(temp_ss[6][0:-1]) * 1.0 / 10000.0
    print Conf.__dict__


# print Conf

def process_data(buf):
    xdata, ydata = [], []
    temp_ss = buf.split()
    print temp_ss
    len = hex2int(temp_ss[25])
    print 'len ', len
    for i in range(26, 26 + len):
        # print i-25,' ',temp_ss[i]
        angle = ((i - 26) * Conf.resolution + 0) * 3.1415926 / 180
        vle = hex2int(temp_ss[i]) / 1000.0
        xdata.append(np.cos(angle) * vle)
        ydata.append(np.sin(angle) * vle)
    return xdata, ydata


s.connect(('192.168.0.2', 2111))
s.send("sRN LMPscancfg")
buf = s.recv(2048)
# process_buf(buf)
process_conf(buf)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set the z axis limits so they aren't recalculated each frame.
ax.set_zlim(0, 10)
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)

# Begin plotting.
wframe = None
tstart = time.time()

X = []
Y = []
Z = []
show_len = 50
while True:
    s.send("sRN LMDscandata")
    buf = s.recv(1500)
    print buf
    if len(buf) < 100:
        continue
    temp_x, temp_y = process_data(buf)
    print temp_x, temp_y
    if len(X) < show_len:
        X.append(temp_x)
        Z.append(temp_y)
        Y.append(len(temp_y) * [len(X) * 0.2])

    if wframe:
        ax.collections.remove(wframe)
    wframe = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
    print X
    print Y
    print Z
    plt.pause(1)

s.close()
