#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# #!/bin/python3
#
# usbdetect.py
#
# Author:  Mauricio Matamoros
# Date:    2022.09.13
# License: MIT
#
# Detects when a USB media is inserted and prints the list of images within
#

import os
import pyudev
from time import sleep
import subprocess as sp

def print_dev_stats(path):
	photos = []
	for file in os.listdir(path):
		if file.endswith(".jpg") \
		or file.endswith(".png"):
			photos.append(file)
	print("{} has {} photos.".format(path, len(photos)))
#end def

def print_dev_info(device):
	print("Device sys_path: {}".format(device.sys_path))
	print("Device sys_name: {}".format(device.sys_name))
	print("Device sys_number: {}".format(device.sys_number))
	print("Device subsystem: {}".format(device.subsystem))
	print("Device device_type: {}".format(device.device_type))
	print("Device is_initialized: {}".format(device.is_initialized))
#end def

def auto_mount(path):
	args = ["udisksctl", "mount", "-b", path]
	sp.run(args)
#end def

def get_mount_point(path):
	args = ["findmnt", "-unl", "-S", path]
	cp = sp.run(args, capture_output=True, text=True)
	out = cp.stdout.split(" ")[0]
	return out
#end def

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem="block", device_type="partition")
while True:
	action, device = monitor.receive_device()
	if action != "add":
		continue
	print_dev_info(device)
	auto_mount("/dev/" + device.sys_name)
	mp = get_mount_point("/dev/" + device.sys_name)
	print("Mount point: {}".format(mp))
	print_dev_stats(mp)
	break
