#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
#
# Author: Mauricio Matamoros
# Date:
#
# ## ############################################################
import smbus2
import struct
import time

# RP2040 I2C device address
SLAVE_ADDR = 0x0A # I2C Address of RP2040

# Name of the file in which the log is kept
LOG_FILE = './temp.log'

# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus2.SMBus(1)

def readTemperature():
	try:
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
		i2c.i2c_rdwr(msg)  # Performs write (read request)
		data = list(msg)   # Converts stream to list
		# list to array of bytes (required to decode)
		ba = bytearray()
		for c in data:
			ba.append(int(c))
		temp = struct.unpack('<f', ba)
		print('Received temp: {} = {}'.format(data, temp))
		return temp
	except:
		return None

def log_temp(temperature):
	try:
		with open(LOG_FILE, 'w+') as fp:
			fp.write('{} {}°C\n'.format(
				time.time(),
				temperature
			))
	except:
		return

def main():
	while True:
		try:
			cTemp = readTemperature()
			log_temp(cTemp)
			time.sleep(1)
		except KeyboardInterrupt:
			return

if __name__ == '__main__':
	main()
