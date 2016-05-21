#!/bin/python3

import sys


time = input().strip()

h = int(time[0:2])
constant = time[2:8]
ampm = time[8:10]
if ampm == 'AM':
	if h == 12:
		print('%02i' % 0 , constant, sep='')
	else:
		print('%02i' % h , constant, sep='')
else:
	if h == 12:
		print('%02i' % h , constant, sep='')
	else:
		print('%02i' % (h+12) , constant, sep='')