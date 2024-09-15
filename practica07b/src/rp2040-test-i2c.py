# ## #############################################################
#
# rp2040-test-i2c.py
#
# Author:  Mauricio Matamoros
# License: MIT
# Date:    2024.05.02
#
# IMPORTANT: Save in RP2040 as main.py
#
# Tests I²C communication between the Raspberry Pi and the RP2040
# receiving a float value.
#
# ## ############################################################
import machine
import ustruct
from utime import sleep_ms, sleep_us
from i2cslave import I2CSlave

# Prints all floats arriving thorugh i2c (slave)
# and replies doubling that number
def main():
    i2c = I2CSlave(address=0x0A)
    print('Slave ready')

    while True:
        # Waits until there are exactly 4 bytes (1 float) in buffer
        while i2c.rxBufferCount() < 4:
            sleep_us(10)
        data = i2c.read()
        pwr = ustruct.unpack("<f", data)
        data = ustruct.pack('<f', pwr * 2)
        i2c.write(data)
        print(f'Master said: {pwr}')
# end def

if __name__ == '__main__':
    main()
