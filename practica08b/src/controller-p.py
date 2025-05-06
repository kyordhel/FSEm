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

DESIRED_TEMPERATURE = 50.0
KP = 1

# RP2040's I2C device address
SLAVE_ADDR = 0x0A # I2C Address of the RP2040

# Initialize the I2C bus;
# RPI version 1 requires smbus.SMBus(0)
i2c = smbus2.SMBus(1)



def readTemperature():
	try:
		# Creates a message object to read 4 bytes from SLAVE_ADDR
		msg = smbus2.i2c_msg.read(SLAVE_ADDR, 4)
		i2c.i2c_rdwr(msg)  # Performs write
		data = list(msg)   # Converts stream to list
		ba = bytearray()
		for c in data:
			ba.append(int(c))
		temp = struct.unpack('<f', ba)
		# print('Received temp: {} = {}'.format(data, temp))
		return temp
	except:
		return None

def writePower(pwr):
	try:
		data = struct.pack('<f', pwr) # Packs number as float
		# Creates a message object to write 4 bytes from SLAVE_ADDR
		msg = smbus2.i2c_msg.write(SLAVE_ADDR, data)
		i2c.i2c_rdwr(msg)  # Performs write
	except:
		pass

def main():
	print("-= P controller =-")
	print("  Desired temperature: {:0.2f}°C".format(DESIRED_TEMPERATURE))

	while True:
		try:
			# Read and report current temperature
			current = readTemperature()
			print("\r  Current temperature: {:0.2f}°C".format(current), end="")
			# Calculate error: E(s) = R(s) - B(s)
			error = DESIRED_TEMPERATURE - current
			# Calculate plant input: V(s) = KP × E(s)
			power = KP * error
			writePower(power)
			# Wait so controller can act.
			sleep(0.25)
		except:
			print("\tError!")
			writePower(0)

if __name__ == '__main__':
	main()
