#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## ###############################################
#
# pwm.py
# Blinks a led on pin 32 using Raspberry Pi's PWM
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
# Initializes virtual board (comment out for hardware deploy)
import virtualboard

# Set up Rpi.GPIO library to use physical pin numbers
GPIO.setmode(GPIO.BOARD)
# Set up pin no. 32 as output and default it to low
GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)
# Set up PWM on pin 32 at 1Hz
pwm = GPIO.PWM(32, 1)
print("Starting pwm")
# Set duty cycle to 50% to blink 500ms on 500ms off
pwm.start(50)
print("Pwm started")
flag = True

# Blink the led
while flag:
	try:
		dutyCycle = int(input("Set duty cycle: "))
		pwm.ChangeDutyCycle(dutyCycle)
	except:
		flag = False
		pwm.ChangeDutyCycle(0)

# Stop the PWM
pwm.stop()
# Reset all ports to its default state (inputs)
GPIO.cleanup()
