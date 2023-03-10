#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# #!/bin/python3
#
# miniusbdetect.py
#
# Author:  Mauricio Matamoros
# Date:    2022.09.13
# License: MIT
#
# Detects when a USB mass storage device is inserted
#

import pyudev

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='block', device_type='partition')
while True:
	action, device = monitor.receive_device()
	if action != 'partition':
		continue
	print(f'Detected device {device.sys_name} on {device.sys_path}')
	break
