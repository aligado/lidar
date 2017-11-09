#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mattest1.py
#  
#  Copyright 2017 alpc32 <alpc32@ALPC>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r', animated=True)
#plt.xlim(-10, 10)
#plt.ylim(-10, 10)

def init():
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    return ln,

def update(frame):
    xdata.append(frame)  
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update,  frames=np.linspace(0, 4*np.pi, 128),
                    init_func=init, blit=True)
plt.show()

