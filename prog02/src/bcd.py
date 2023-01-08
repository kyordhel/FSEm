#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## ###############################################
#
# pwm.py
# Controls a 7-segments display using Raspberry Pi
# and a 74LS47 driver
#
# Autor: Mauricio Matamoros
# License: MIT
#
# ## ###############################################

# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import Raspberry Pi's GPIO control library
import RPi.GPIO as GPIO
# Imports sleep functon
from time import sleep
# Initializes virtual board (comment for hardware deploy)
import virtualboard

# Set up Rpi.GPIO library to use physical pin numbers
GPIO.setmode(GPIO.BOARD)
# Set up pins 36, 38, 40 and 37 as output and default them to low
GPIO.setup(36, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(38, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW)

def bcd7(num):
	"""Converts num to a BCD representation"""
	GPIO.output(36, GPIO.HIGH if (num & 0x00000001) > 0 else GPIO.LOW )
	GPIO.output(38, GPIO.HIGH if (num & 0x00000002) > 0 else GPIO.LOW )
	GPIO.output(40, GPIO.HIGH if (num & 0x00000004) > 0 else GPIO.LOW )
	GPIO.output(37, GPIO.HIGH if (num & 0x00000008) > 0 else GPIO.LOW )

# Request a number and send it to the display
flag = True
while flag:
	try:
		num = int(input("Enter int between 0 and 15: "))
		bcd7(num)
	except:
		flag = False

# Reset all ports to its default state (inputs)
GPIO.cleanup()
