#!/bin/sh
while true;
do
  count=$(ps -ef | grep -c start.py) #查找当前的进程中，计算server程序的数量
  if [ $count -lt 4 ]; then        #判断服务器进程的数量是否小于4（根据实际填上你的服务器进程数量）
    ps -efww|grep -w 'start.py'|grep -v grep|cut -c 9-15|xargs kill -9
    # server start                   #这里填入需要重启的服务器进程
    cd '/media/psf/share/lidar/main'
    python start.py
  fi
  sleep 2                          #睡眠2s，周期性地检测服务器程序是不是崩溃了
done