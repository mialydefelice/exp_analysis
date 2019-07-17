'''
The purrpose of this file is to rename an entire directory to 
be used with the FIJI implementation of MoMA.
'''
import os
import re

for fileName in os.listdir("."):
	channel_num = re.search('channel(.+?)_position')
	time_num = re.search('time00000(.+?)_z')
	c_t = 'c0' + channel_num + time_num
    os.rename(fileName, fileName.replace('z000', c_t))
