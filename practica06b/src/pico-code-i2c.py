# ## #############################################################
#
# src/pico-code-iic.py
#
# Author: Mauricio Matamoros
#
# Reads temperature from ADC using an LM35 (dummy) and sends
# it via I²C bus
#
# Pro-Tip: rename as main.py in the RP2040
# Pro-Tip: Remove anchor and main functions in i2cslave.py
#
# ## ############################################################
from i2cslave import I2CSlave
from utime import sleep_ms, sleep_us
import ustruct

VAREF          = 2.7273
I2C_SLAVE_ADDR = 0x0A


def main():
	setup()
	while True:
		# 1. Get temperature
		temperature = read_temp()
		# 2. Convert temperature from pyfloat to bytes
		data = ustruct.pack('<f', temperature)

		# 3. Check if Master requested data
		if i2c.waitForRdReq(timeout=0):
			# If so, send the temperature to Master
			i2c.write(data)
		# end if

		# 3. Check if Master sent data
		if i2c.waitForData(timeout=0):
			# If so, print it
			rcv = i2c.read()
			print( rcv.decode('utf-8') )
		# end if
# end def


def read_temp():
	# '''Reads temperature in C from the ADC'''
	return 25.0
# end def


def setup():
	global i2c, adcm, adcp
	i2c = I2CSlave(address=I2C_SLAVE_ADDR)
	adcm = machine.ADC(0)         # Init ADC0
	adcp = machine.ADC(1)         # Init ADC1
# end def


if __name__ == '__main__':
	main()
