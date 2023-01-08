#!/usr/bin/env python3
# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)
pwm = GPIO.PWM(32, 1000)

pwm.start(50)
flag = True
while flag:
	try:
		dutyCycle = int(input("Duty cycle: "))
		pwm.ChangeDutyCycle(dutyCycle)
	except:
		flag = False
		pwm.ChangeDutyCycle(0)
	#end try
#end while
pwm.stop()
GPIO.cleanup()

