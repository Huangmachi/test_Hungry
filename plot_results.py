# Copyright (C) 2016 Huang MaChi at Chongqing University
# of Posts and Telecommunications, Chongqing, China.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import re
import matplotlib.pyplot as plt
import numpy as np


def read_file(file_name, delim=','):
	"""
		Read the bwmng.txt file.
	"""
	read_file = open(file_name, 'r')
	lines = read_file.xreadlines()
	lines_list = []
	for line in lines:
		line_list = line.strip().split(delim)
		lines_list.append(line_list)
	read_file.close()

	# Remove the last second's statistics, because they are mostly not intact.
	last_second = lines_list[-1][0]
	_lines_list = lines_list[:]
	for line in _lines_list:
		if line[0] == last_second:
			lines_list.remove(line)

	return lines_list

def get_total_throughput(total_throughput):
	"""
		total_throughput = {0:x, 1:x, 2:x, ...}
	"""
	lines_list = read_file('./results/bwmng.txt')
	first_second = int(lines_list[0][0])
	column_bytes_out = 6   # bytes_out
	switch = 's2'
	sw = re.compile(switch)
	realtime_throught = {}

	for i in xrange(121):
		if not total_throughput.has_key(i):
			total_throughput[i] = 0

	for i in xrange(121):
		if not realtime_throught.has_key(i):
			realtime_throught[i] = 0

	for row in lines_list:
		iface_name = row[1]
		if sw.match(iface_name):
			if int(iface_name[-1]) <= 3:   # Choose host-connecting interfaces only.
				if (int(row[0]) - first_second) <= 120:   # Take the good values only.
					realtime_throught[int(row[0]) - first_second] += float(row[column_bytes_out]) * 8.0 / (10 ** 6)   # Mbit

	for i in xrange(121):
		for j in xrange(i+1):
			total_throughput[i] += realtime_throught[j]   # Mbit

	return total_throughput

def get_value_list(value_dict):
	"""
		Get the values from the "total_throughput" data structure.
	"""
	value_list = []
	for i in xrange(121):
		value_list.append(value_dict[i])
	return value_list

def get_realtime_speed(switch):
	"""
		Get realtime speed of individual flow.
	"""
	realtime_speed = {}
	lines_list = read_file('./results/bwmng.txt')
	first_second = int(lines_list[0][0])
	column_bytes_out_rate = 2   # bytes_out/s
	sw = re.compile(switch)

	for i in xrange(121):
		if not realtime_speed.has_key(i):
			realtime_speed[i] = 0

	for row in lines_list:
		iface_name = row[1]
		if sw.match(iface_name):
			if (int(row[0]) - first_second) <= 120:   # Take the good values only.
				realtime_speed[int(row[0]) - first_second] += float(row[column_bytes_out_rate]) * 8.0 / (10 ** 6)   # Mbit/s

	return realtime_speed

def plot_results():
	"""
		Plot the results:
		1. Plot total throughput
		2. Plot realtime speed of individual flow
	"""
	bandwidth = 10.0   # (unit: Mbit/s)
	utmost_throughput = bandwidth * 120
	total_throughput = {}
	total_throughput = get_total_throughput(total_throughput)

	# 1. Plot total throughput.
	fig = plt.figure()
	fig.set_size_inches(12, 6)
	x = np.arange(0, 121)
	y = get_value_list(total_throughput)
	plt.plot(x, y, 'r-', linewidth=2)
	plt.xlabel('Time (s)', fontsize='x-large')
	plt.xlim(0, 120)
	plt.xticks(np.arange(0, 121, 30))
	plt.ylabel('Total Throughput\n(Mbit)', fontsize='x-large')
	plt.ylim(0, utmost_throughput)
	plt.yticks(np.linspace(0, utmost_throughput, 11))
	plt.grid(True)
	plt.savefig('./results/1.total_throughput.png')

	# 2. Plot realtime speed of individual flow.
	fig = plt.figure()
	fig.set_size_inches(12, 6)
	x = np.arange(0, 121)
	realtime_speed1 = get_realtime_speed('s2-eth1')
	y1 = get_value_list(realtime_speed1)
	realtime_speed2 = get_realtime_speed('s2-eth2')
	y2 = get_value_list(realtime_speed2)
	realtime_speed3 = get_realtime_speed('s2-eth3')
	y3 = get_value_list(realtime_speed3)
	plt.plot(x, y1, 'r-', linewidth=2, label="Flow1")
	plt.plot(x, y2, 'g-', linewidth=2, label="Flow2")
	plt.plot(x, y3, 'b-', linewidth=2, label="Flow3")
	plt.xlabel('Time (s)', fontsize='x-large')
	plt.xlim(0, 120)
	plt.xticks(np.arange(0, 121, 30))
	plt.ylabel('Realtime Speed of Individual Flow\n(Mbit/s)', fontsize='x-large')
	plt.ylim(0, bandwidth)
	plt.yticks(np.linspace(0, bandwidth, 11))
	plt.legend(loc='upper right', ncol=3, fontsize='small')
	plt.grid(True)
	plt.savefig('./results/2.realtime_speed_of_individual_flow.png')

	# 3. Plot realtime throughput.
	fig = plt.figure()
	fig.set_size_inches(12, 6)
	x = np.arange(0, 121)
	realtime_speed = get_realtime_speed('s2-eth[1-3]')
	y = get_value_list(realtime_speed)
	plt.plot(x, y, 'r-', linewidth=2)
	plt.xlabel('Time (s)', fontsize='x-large')
	plt.xlim(0, 120)
	plt.xticks(np.arange(0, 121, 30))
	plt.ylabel('Realtime Throughput\n(Mbit/s)', fontsize='x-large')
	plt.ylim(0, bandwidth)
	plt.yticks(np.linspace(0, bandwidth, 11))
	plt.grid(True)
	plt.savefig('./results/3.realtime_throught.png')


if __name__ == '__main__':
	plot_results()
