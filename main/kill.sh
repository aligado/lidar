#!/bin/sh
ps -efww|grep -w 'start.py'|grep -v grep|cut -c 9-15|xargs kill -9