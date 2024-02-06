# ## #############################################################
#
# i2cslave.py
#
# Author:  Mauricio Matamoros
# License: MIT
# Date:    2024.02.03
#
# Library to use the raspberry pico as a I²C slave device.
# Supports only 7-bit addresses, and reads and writes in bulks.
# Does not support RPC, transactions, or any other weird stuff.
#
# Due to Python limitations it does NOT support interrupts or IRQs.
# The use of DMA is future work.
#
# Stand-Alone testing:
# Connect GPIO0 to GPIO2
# Connect GPIO1 to GPIO3
# Connect VCC to both, GPIO0 and GPIO1 via a 10K resistor
#
# ## ############################################################
import machine
from utime import sleep_ms, sleep_us

# Constants from the RP2040 Datasheet
__IO_BANK0_BASE         = 0x40014000 # GPIO registers base addresses
__I2C0_BASE             = 0X40044000 # I²C0 registers base addresses
__I2C1_BASE             = 0X40048000 # I²C1 registers base addresses
__ATOM_RW               = 0x0000
__ATOM_XOR              = 0x1000
__ATOM_SET              = 0x2000
__ATOM_CLR              = 0x3000
__IC_CON                = 0x00 # I²C Control Register
__IC_TAR                = 0x04 # I²C Target Address Register
__IC_SAR                = 0x08 # I²C Slave Address Register
__IC_DATA_CMD           = 0x10 # I²C Rx/Tx Data Buffer and Command Register
__IC_SS_SCL_HCNT        = 0x14 # Standard Speed I²C Clock SCL High Count Register
__IC_SS_SCL_LCNT        = 0x18 # Standard Speed I²C Clock SCL Low Count Register
__IC_FS_SCL_HCNT        = 0x1c # Fast Mode or Fast Mode Plus I²C Clock SCL High Count Register
__IC_FS_SCL_LCNT        = 0x20 # Fast Mode or Fast Mode Plus I²C Clock SCL Low Count Register
__IC_INTR_STAT          = 0x2c # I²C Interrupt Status Register
__IC_INTR_MASK          = 0x30 # I²C Interrupt Mask Register
__IC_RAW_INTR_STAT      = 0x34 # I²C Raw Interrupt Status Register
__IC_RX_TL              = 0x38 # I²C Receive FIFO Threshold Register
__IC_TX_TL              = 0x3c # I²C Transmit FIFO Threshold Register
__IC_CLR_INTR           = 0x40 # Clear Combined and Individual Interrupt Register
__IC_CLR_RX_UNDER       = 0x44 # Clear RX_UNDER Interrupt Register
__IC_CLR_RX_OVER        = 0x48 # Clear RX_OVER Interrupt Register
__IC_CLR_TX_OVER        = 0x4c # Clear TX_OVER Interrupt Register
__IC_CLR_RD_REQ         = 0x50 # Clear RD_REQ Interrupt Register
__IC_CLR_TX_ABRT        = 0x54 # Clear TX_ABRT Interrupt Register
__IC_CLR_RX_DONE        = 0x58 # Clear RX_DONE Interrupt Register
__IC_CLR_ACTIVITY       = 0x5c # Clear ACTIVITY Interrupt Register
__IC_CLR_STOP_DET       = 0x60 # Clear STOP_DET Interrupt Register
__IC_CLR_START_DET      = 0x64 # Clear START_DET Interrupt Register
__IC_CLR_GEN_CALL       = 0x68 # Clear GEN_CALL Interrupt Register
__IC_ENABLE             = 0x6c # I²C ENABLE Register
__IC_STATUS             = 0x70 # I²C STATUS Register
__IC_TXFLR              = 0x74 # I²C Transmit FIFO Level Register
__IC_RXFLR              = 0x78 # I²C Receive FIFO Level Register
__IC_SDA_HOLD           = 0x7c # I²C SDA Hold Time Length Register
__IC_TX_ABRT_SOURCE     = 0x80 # I²C Transmit Abort Source Register
__IC_SLV_DATA_NACK_ONLY = 0x84 # Generate Slave Data NACK Register
__IC_DMA_CR             = 0x88 # DMA Control Register
__IC_DMA_TDLR           = 0x8c # DMA Transmit Data Level Register
__IC_DMA_RDLR           = 0x90 # DMA Transmit Data Level Register
__IC_SDA_SETUP          = 0x94 # I²C SDA Setup Register
__IC_ACK_GENERAL_CALL   = 0x98 # I²C ACK General Call Register
__IC_ENABLE_STATUS      = 0x9c # I²C Enable Status Register
__IC_FS_SPKLEN          = 0xa0 # I²C SS, FS or FM+ spike suppression limit
__IC_CLR_RESTART_DET    = 0xa8 # Clear RESTART_DET Interrupt Register
__IC_COMP_PARAM_1       = 0xf4 # Component Parameter Register 1
__IC_COMP_VERSION       = 0xf8 # I²C Component Version Register
__IC_COMP_TYPE          = 0xfc # I²C Component Type Register

class I2CSlave():
#'''
#	This class allows to use the RP2040 as an I²C slave device.
#	Since there is no support for this in MicroPython, we do this
#	at register-level with machine.memXX[ADDR] = Value
#'''


	def __init__(self, id=0, address=0x27, sda=None, scl=None):
		if id > 1: raise ValueError('Unsupported')
		elif id == 0:
			if sda is None: sda = 0 #sda = machine.Pin(0)
			if scl is None: scl = 1 #scl = machine.Pin(1)
			if sda not in [0, 4, 8, 12, 16, 20]:
				raise ValueError('Invalid pin number for sda')
			if scl not in [1, 5, 9, 13, 17, 21]:
				raise ValueError('Invalid pin number for scl')
		else: # id == 1:
			if sda is None: sda = 2 #sda = machine.Pin(2)
			if scl is None: scl = 3 #scl = machine.Pin(3)
			if sda not in [2, 6, 10, 14, 18, 26]:
				raise ValueError('Invalid pin number for sda')
			if scl not in [3, 7, 11, 15, 19, 27]:
				raise ValueError('Invalid pin number for scl')

		if address < 0 or address > 0x7f:
			raise ValueError('Address out of range (7bit addresses only)')

		self._sda  = sda
		self._scl  = scl
		self._addr = address
		self._base = __I2C0_BASE if id == 0 else __I2C1_BASE

		# Setup pins
		self.__setupPin(sda)
		self.__setupPin(scl)

		# From pp 453
		# 1. Disable the DW_apb_i2c by writing a '0' to IC_ENABLE.ENABLE (bit 0).
		self.__regClr(__IC_ENABLE, 0x0001)
		# 2. Write to the IC_SAR register (bits 9:0) to set the slave address.
		self.__regClr(__IC_SAR, 0x01ff)
		self.__regSet(__IC_SAR, address)

		# 3. Set Configuration (pp 466, bits 7-0)
		# Clear bits 6, 3 and 0 (Disable slave, 10 bits, Master mode)
		self.__regClr(__IC_CON, 0x0049)


		# 4. Re-enable I²C  (bit 0)
		self.__regSet(__IC_ENABLE, 0x0001)

		self.__initialized = True
	# end def

	def __setupPin(self, pin):
		# Page 243, Table 282: Each GPIO pin uses 8 bytes: 4 status, 4 control
		# To setup we clear and set the 32-bit Control register. Offset = 4
		gpioaddr = __IO_BANK0_BASE + 8 * pin + 4
		machine.mem32[ gpioaddr | __ATOM_CLR ] = 0x1f # FUNCSEL mask
		machine.mem32[ gpioaddr | __ATOM_SET ] = 0x03 # Attach pin to I2C
	# end def

	def __regClr(self, reg, mask):
		machine.mem32[self._base | __ATOM_CLR | reg] = mask
	# end def

	def __regSet(self, reg, mask):
		machine.mem32[self._base | __ATOM_SET | reg] = mask
	# end def

	def __regRead(self, reg, andmask=0xffffffff):
		return machine.mem32[self._base | __ATOM_RW | reg] & andmask

	def __regWrite(self, reg, value):
		machine.mem32[self._base | __ATOM_RW  | reg] = value
	# end def

	def __regXor(self, reg, mask):
		machine.mem32[self._base | __ATOM_XOR | reg] = mask
	# end def

	@property
	def id(self):
		return 0 if self._base == __I2C0_BASE else 1
	# end def

	@property
	def sda(self):
		return self._sda
	# end def

	@property
	def scl(self):
		return self._scl
	# end def

	@property
	def address(self):
		return self._addr
	# end def


	def deInit(self):
		self.__initialized = False
		#'''Turn off the I2C bus.'''
		# 1. Disable the DW_apb_i2c by writing a '0' to IC_ENABLE.ENABLE (bit 0).
		self.__regClr(__IC_ENABLE, 0x0001)
		# 2. Clear the IC_SAR register
		self.__regClr(__IC_SAR, 0x01ff)
		# 3. Clear Configuration (pp 466, bits 7-0)
		self.__regClr(__IC_CON, 0x0049)
		# Set bits 6 and 0 (Disable slave, Master mode)
		self.__regSet(__IC_CON, 0x0021)
		# 4. Re-enable I²C  (bit 0)
		self.__regSet(__IC_ENABLE, 0x0001)
		self._sda  = None
		self._scl  = None
		self._addr = None
		self._base = None
	# end def

	def idle(self):
		return not self.__regRead(__IC_STATUS, 0x01)
	# end def

	def rxBufferCount(self):
		return self.__regRead(__IC_RXFLR, 0x1f)
	# end def

	def rxBufferEmpty(self):
		return not self.__regRead(__IC_STATUS, 0x08)
	# end def

	def rxBufferFull(self):
		return self.__regRead(__IC_STATUS, 0x10)
	# end def

	def txBufferCount(self):
		return self.__regRead(__IC_TXFLR, 0x10)
	# end def

	def txBufferEmpty(self):
		return not self.__regRead(__IC_STATUS, 0x04)
	# end def

	def txBufferFull(self):
		return not self.__regRead(__IC_STATUS, 0x02)
	# end def

	def read(self):
		#'''Blocks until the Master sends some data,
		#   then retrieves the data from the buffer'''
		if not self.__initialized: raise IOError('Uninitialized')
		# Wait until data arrives to the buffer
		while not self.__regRead(__IC_STATUS, 0x08) and self.__regRead(__IC_RXFLR, 0x1f) < 1:
			sleep_us(10)
		# Get number of bytes in buffer, allocate memory and retrieve
		bytecount = self.__regRead(__IC_RXFLR, 0x1f)
		ba = bytearray(bytecount)
		for i in range(bytecount):
			ba[i] = self.__regRead(__IC_DATA_CMD, 0xff)
		return ba
	# end def

	def readByte(self):
		#'''Blocks until the Master sends some data,
		#   then retrieves the data from the buffer'''
		if not self.__initialized: raise IOError('Uninitialized')
		# Wait until data arrives to the buffer
		while not self.__regRead(__IC_STATUS, 0x08):
			sleep_us(10)
		# Return first byte in the buffer
		return self.__regRead(__IC_DATA_CMD, 0xff)
	# end def

	def write(self, ba):
		#'''Blocks until the Master requests data, then writes the data
		#   in the buffer. Lags until all the data has been written.
		#   We can't just put the data in the txBuffer and return (async)
		#   bc upon the RD_REQ arrival a TX_ABRT is generated and the
		#   txBuffer is automatically flushed (see 4.3.10.1.2, pp. 454)'''
		if not self.__initialized: raise IOError('Uninitialized')
		if not isinstance(ba, (bytes, bytearray)): raise ValueError('An array of bytes is required')
		for b in ba:
			self.writeByte(b)
	# end def

	def writeByte(self, b):
		#'''Blocks until the Master requests byte, then writes the byte
		#   in the buffer.
		#   We can't just put the data in the txBuffer and return (async)
		#   bc upon the RD_REQ arrival a TX_ABRT is generated and the
		#   txBuffer is automatically flushed (see 4.3.10.1.2, pp. 454)'''
		if not self.__initialized: raise IOError('Uninitialized')
		# 1. Wait for the RD_REQ signal (bit 5)
		while not self.__regRead(__IC_RAW_INTR_STAT, 0x20):
			sleep_us(10)
		# 2. Clear the ABORT register that would abort a transmission
		self.__regClr(__IC_CLR_TX_ABRT, 0x01)
		# 3. Clear the read request by reading this register
		self.__regRead(__IC_CLR_RD_REQ)
		# 4. Wait until there is space in the Tx Buffer
		while not self.__regRead(__IC_STATUS, 0x02):
			sleep_us(10)
		self.__regWrite(__IC_DATA_CMD, b & 0xff)
	# end def

	def waitForData(self, timeout=-1):
		# '''Blocks until data is received in the rxBuffer
		#    Returns true if data arrived before the timeout, false otherwise.
		# '''
		if not self.__initialized: raise IOError('Uninitialized')
		while self.rxBufferEmpty() and (timeout > 0):
			timeout-= 1
			sleep_ms(1)
		return not self.rxBufferEmpty()
	# end def

	def waitForRdReq(self, timeout=-1):
		# '''Awaits for a read request for up to timeout ms.
		#    Returns true if the read requests arrived, false otherwise.
		# '''
		if not self.__initialized: raise IOError('Uninitialized')
		while (self.__regRead(__IC_RAW_INTR_STAT, 0x20) != 0) and (timeout > 0):
			timeout-= 1
			sleep_ms(1)
		return self.__regRead(__IC_RAW_INTR_STAT, 0x20)
	# end def
# end class


__running = True
def main1():
	import random, ustruct
	i2c = machine.I2C(1, sda=machine.Pin(2), scl=machine.Pin(3), freq=400_000)
	print('Master ready')
	devices = [hex(d) for d in i2c.scan()]
	print('I2C devices:', devices)
	ba = bytearray(2)

	while __running:
		ba[0] = random.randint(0, 255)
		ba[1] = random.randint(0, 255)
		i2c.writeto(0x55, ba)
		sleep_ms(100) # Wait until slave finishes printing
		res = i2c.readfrom(0x55, 2)
		res = ustruct.unpack("<h", res)[0]
		print('[Master] Slave says:', res)
		sleep_ms(3000)
# end def



def main0():
	import _thread, ustruct
	_thread.start_new_thread(main1, [])

	i2c = I2CSlave(address=0x55)
	print('Slave ready')
	while __running:
		data = i2c.read()
		a, b = ustruct.unpack("<BB", data)
		print(f'[Slave ] Master says: {a} + {b}')
		data = ustruct.pack('<h', a + b)
		i2c.write(data)
		sleep_ms(1000)
# end def

if __name__ == '__main__':
	try:
		main0()
	except KeyboardInterrupt:
		__running = False
	__running = False
