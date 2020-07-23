#!/usr/bin/python2

import subprocess
import sys

if len(sys.argv) < 2:
	exit()
n = sys.argv[1]
print('started', n)

# fd = open('/home/akalend/projects/myvpn/log/out.log','a')
process = subprocess.Popen(['/usr/bin/python2', '/home/akalend/projects/myvpn/master.py', n], stdin=None, stdout=None, stderr=None)
print('finish')
# print(code) # 0