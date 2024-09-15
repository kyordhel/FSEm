# ## #############################################################
#
# rp2040-sol.py
#
# Author:  Mauricio Matamoros
# License: MIT
# Date:    2024.05.02
#
# IMPORTANT: Save in RP2040 as main.py
#
# Practice solution
#
# ## ############################################################
import rp2
import ustruct
from machine import Pin
from utime import sleep_ms, sleep_us

from i2cslave import I2CSlave

zxpin = Pin(0, Pin.IN)
trpin = Pin(1, Pin.OUT)
i2c = I2CSlave(address=0x0A)


def main():
    setup()
    print('Slave ready')

    while True:
        # Waits until there are exactly 4 bytes (1 float) in buffer
        while i2c.rxBufferCount() < 4:
            sleep_us(10)
        data = i2c.read()
        pwr  = ustruct.unpack("<f", data)
        ticks  = power2SMticks(pwr)
        sm.put(ticks)
        rpwr = smTicks2Power(ticks)
        data = ustruct.pack('<f', rpwr)
        i2c.write(data)
        print(f'Power in: {pwr} | Real power: {rpwr:0.2f}')
# end def


def setup():
    sm = rp2.StateMachine(0,
        dimmer,
        freq=20_000,
        in_base=zxpin,
        set_base=trpin
    )
sm.active(1)
# end def


# At 20kHz the each state machine step takes 50us
# For an (almost) whole cycle of 8.3ms, the timeout must be set
# to (8300 - Δt - 20*50)/50 = 146 where Δt is the gap between the
# zx edges. Δt is neglected by the delay in the voltage
# stabilization delay that triggers the SM.
def power2SMticks(power):
    if power <= 0:   return 146
    if power >= 100: return   0
    return 146 - int(146 * power / 100)
# end def


def smTicks2Power(tick_count):
    return 100 * (1 - tick_count / 146.0)
# end def


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def dimmer():
    # 0. Setup: Preload X with timeout, set TRIAC pin low
    set(pin, 0)
    pull()
    mov(x, osr)

    # Main loop
    label('waitzx')
    wrap_target()
    wait(0, pin, 0)
    pull(noblock)
    mov(x, osr)
    mov(y, x)
    wait(1, pin, 0)
    nop() [17]
    label('delay')
    jmp(y_dec, 'delay')
    set(pins, 1)
    set(pins, 0)
    jmp('waitzx')
    wrap()
# end def


if __name__ == '__main__':
    main()
