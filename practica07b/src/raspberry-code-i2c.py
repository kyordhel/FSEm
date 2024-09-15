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

# Arduino's I2C device address
SLAVE_ADDR = 0x0A # I2C Address of RP2040

# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus2.SMBus(1)

def readPower():
	try:
		# Creates a message object to read 4 bytes from SLAVE_ADDR
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
		i2c.i2c_rdwr(msg)  # Performs write
		data = list(msg)   # Converts stream to list
		# list to array of bytes (required to decode)
		ba = bytearray()
		for c in data:
			ba.append(int(c))
		pwr = struct.unpack('<f', ba)
		# print('Received power: {} = {}'.format(data, pwr))
		return pwr
	except:
		return -1

def writePower(pwr):
	try:
		data = struct.pack('<f', pwr) # Packs number as float
		# Creates a message object to write 4 bytes from SLAVE_ADDR
		msg = smbus2.i2c_msg.write(SLAVE_ADDR, data)
		i2c.i2c_rdwr(msg)  # Performs write
	except:
		pass

def main():
	while True:
		try:
			power = input("Power? ")
			power = float(power)
			if power >= 0 and power <= 100:
				writePower(power)
				print("\tPower set to {}".format(readPower()))
			else:
				print("\tInvalid!")
		except:
			print("\tInvalid!")

if __name__ == '__main__':
	main()
