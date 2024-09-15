# ## #############################################################
#
# rp2040-test-zx.py
#
# Author:  Mauricio Matamoros
# License: MIT
# Date:    2024.05.02
#
# IMPORTANT: Save in RP2040 as main.py
#
# Tests the zero-cross detection
#
# ## ############################################################
from machine import Pin, Timer
from utime import sleep_us

zxcount = 0
flag    = False
zxpin   = 0
timer   = None


def setup():
    global zxpin, timer
    zxpin  = Pin(zxpin, Pin.IN)
    zxpin.irq(trigger=Pin.IRQ_FALLING, handler=zxhandle)
    timer  = Timer(period=1000, mode=Timer.PERIODIC, callback=timerHandle)
#end def


def main():
    setup()
    print('Running')
    while True:
        mainloop()
#end def


def mainloop():
    global flag, zxcount
    if not flag:
        # Slack until next interrupt
        sleep_us(10)
        return
    flag = not flag
    print('Count: ', zxcount)
    zxcount = 0
#end def


def zxhandle(pin):
    global zxcount
    zxcount+= 1
#end def


def timerHandle(tmr):
    global flag
    flag = True
#end def

if __name__ == '__main__':
    main()


