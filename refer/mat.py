#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mat.py
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

# -*- coding: utf-8 -*-  
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
axes1 = fig.add_subplot(111)
line, = axes1.plot(np.random.rand(10))

# 因为update的参数是调用函数data_gen,所以第一个默认参数不能是framenum
def update(data):
    line.set_ydata(data)
    return line,


# 每次生成10个随机数据  
def data_gen():
    while True:
        yield np.random.rand(10)


ani = animation.FuncAnimation(fig, update, data_gen, interval=2 * 1000)
plt.show()
