import math
import time
from ctypes import c_int32
from multiprocessing import Queue
# from matplotlib import pyplot as plt     

'''
fig = plt.figure()  
ax = fig.add_subplot(1,1,1,xlim=(-2000, 2000), ylim=(-800, 800))
line, = ax.plot([], [], lw=2)
'''

frame_queue = Queue()

def hex2int(hex_int):
    return c_int32(int(hex_int, 16)).value

def process_data(buf):
    PI = 3.1415926
    xdata, ydata = [], []
    buf_len = len(buf)
    if buf_len < 26:
        return [], []
    num_len = hex2int(buf[25])
    print('len ', num_len)
    end = min(26+num_len, buf_len)
    height = [6666]*6
    for i in range(26, end):
        angle = ((i - 26) * 0.5 + 0) * PI / 180.0
        vle = hex2int(buf[i]) / 10.0
        if vle < 100:
            vle = 0
        temp_x = math.cos(angle) * vle
        temp_y = math.sin(angle) * vle
        if temp_x < -1600:
            temp_x = -1600
        elif temp_x > 1600:
            temp_x = 1600
        temp_x = int(temp_x)
        if temp_y < 0:
            temp_y = 0
        elif temp_y > 800:
            temp_y = 800
        temp_y = int(temp_y)
        xdata.append(temp_x)
        ydata.append(temp_y)
        for lane_index in range(0, 6):
            if temp_x >= -1200+lane_index*400 and temp_x <= -1200+(lane_index+1)*400:
                if temp_y>50 and temp_y < height[lane_index]:
                    height[lane_index] = temp_y

    return xdata, ydata, height

# fp = open('txt/20171120083047.txt', 'r+')
fp = open('txt/20171108141511.txt', 'r+')
begin_flag = 'sSN'
end_flag = '0'
log_lines = fp.readlines()
fp.close()
index = 0

def read_frame(oo=0):
    global index
    print('index', index)
    if index > len(log_lines)-1 or index < -1:
        index = 0
    log_line = log_lines[index].split()
    frame = log_line
    if frame[0] == begin_flag:
        if frame[-1] != end_flag:
            log_line_next = log_lines[index+1].split()
            if log_line_next[-1] == end_flag:
                frame = frame + log_line_next
                index += 2
            else:
                index += 1
        else:
            index += 1
    else:
        index += 1
        return {'x': [], 'y': [], 'height': [], 'widh': []}

    lx, ly, height = process_data(frame)

    return {'x': lx, 'y': ly, 'height': height}

def read():
    for i in range(len(log_lines)):
        print('index', i)
        log_line = log_lines[i].split()
        frame = log_line
        if frame[0]!=begin_flag: # or frame[-1]!=end_flag:
            print(frame[0])
            continue
        lx, ly = process_data(frame)
        '''
        line.set_data(lx, ly)    
        ax.legend()
        plt.pause(0.5)
        '''
        # frame_queue.put({'x': lx, 'y': ly})
        # print lx, ly
        # time.sleep(10)

if __name__ == '__main__':
    read()