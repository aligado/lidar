import numpy as np     
from matplotlib import pyplot as plt     
from matplotlib import animation     
    
LaneNum = 6
fig = plt.figure()   
# first set up the figure, the axis, and the plot element we want to animate     
ax = []
line = []

fig2 = plt.figure('2')  
# ax2 = fig2.add_subplot(1,1,1,xlim=(0, 2), ylim=(-4, 4))
ax2 = fig2.add_subplot(1,1,1,xlim=(-1200, 1200), ylim=(-8, 8))
line2, = ax2.plot([], [], lw=2)

for index in range(0, 6):
    ax.append(fig.add_subplot(2,3,index+1,xlim=(500, 500), ylim=(0, 500), label='aa'))

for index in range(0, 6):
    temp, = ax[index].plot([], [], lw=2)
    line.append(temp)

def init():    
    for index in range(0, 6):
        line[index].set_data([], [])    
    return line[0],line[1],line[2],line[3],line[4],line[5],   

# animation function.  this is called sequentially    
def animate(i):  
    x = np.linspace(0, 2, 100)     
    y = np.sin(2 * np.pi * (x - 0.01 * i))    

    for index in range(0, 6):
        line[index].set_data(x, y)    

    return line[0],line[1],line[2],line[3],line[4],line[5],   

# anim1=animation.FuncAnimation(fig, animate, init_func=init,  frames=50, interval=10)    
    # First set up the figure, the axis, and the plot element we want to animate  

from ctypes import c_int32
def hex2int(hex_int):
    return c_int32(int(hex_int, 16)).value
def process_data(buf):
    xdata, ydata = [], []
    temp_ss = buf.split()
    print temp_ss
    len = hex2int(temp_ss[25])
    print 'len ', len
    for i in range(26, 26 + len):
        # print i-25,' ',temp_ss[i]
        angle = ((i - 26) * 0.5 + 0) * 3.1415926 / 180
        vle = hex2int(temp_ss[i]) / 1000.0
        xdata.append(np.cos(angle) * vle)
        ydata.append(np.sin(angle) * vle)
    return xdata, ydata

fp = open('txt/20171108101000.txt', 'r+')
log_lines = fp.readlines()
fp.close()
for i in range(50):
    x = np.linspace(0, 2, 100)     
    y = np.sin(2 * np.pi * (x - 0.01 * i))    
    for index in range(0, 6):
        line[index].set_data(x, y)    
        ax[index].legend()
    lx, ly = process_data(log_lines[i])
    line2.set_data(lx, ly)    
    ax2.legend()
    plt.pause(0.5)

'''
fig2 = plt.figure('2')  
ax2 = fig2.add_subplot(1,1,1,xlim=(0, 2), ylim=(-4, 4))  
line2, = ax2.plot([], [], lw=2)  

# initialization function: plot the background of each frame  
def init2():  
    line2.set_data([], [])  
    return line2,  

# animation function.  This is called sequentially  
# note: i is framenumber  
def animate2(i):  
    x = np.linspace(0, 2, 1000)  
    y = np.sin(2 * np.pi * (x - 0.01 * i))  
    line2.set_data(x, y)  
    return line2,  

# call the animator.  blit=True means only re-draw the parts that have changed.  
anim2 = animation.FuncAnimation(fig2, animate2, init_func=init2,  
                            frames=200, interval=20, blit=True)  
    
    #anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])  
print 'hello2'
plt.show()
'''