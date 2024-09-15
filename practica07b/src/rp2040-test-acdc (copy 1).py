# ## #############################################################
#
# rp2040-test-acdc.py
#
# Author:  Mauricio Matamoros
# License: MIT
# Date:    2024.05.02
#
# IMPORTANT: Save in RP2040 as main.py
#
# Tests the whole AC/DC circuit
#
# ## ############################################################
from machine import Pin
from utime import sleep_ms
import rp2

zxpin = Pin(0, Pin.IN)
trpin = Pin(1, Pin.OUT)

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def dimmer():
    # 0. Setup: Preload X with timeout, set TRIAC pin low
    set(pin, 0)
    pull()                      # Loads OSR with data
    mov(x, osr)                 # puts OSR contents in X
    
    # Main loop
    label('waitzx')
    wrap_target()
    
    # 1. Wait for zero cross falling edge
    wait(0, pin, 0)
    
    # 2. Update timeout and write it to Y (150us).
    pull(noblock)           # Loads OSR with data
    mov(x, osr)             # puts OSR contents in X
    mov(y, x)               # puts X contents in Y
    
    # 3. Wait for zero cross rising edge
    wait(1, pin, 0)
    nop()               [17]# When V is low, the TRIAC
                            # pulse needs to be wider.
                            # This delay patches it.

    # 4. Wait timeout (until Y is zero) before sending
    # the ON pulse. Each pulse is 50us
    label('delay')
    jmp(y_dec, 'delay')

    # 5. Send a 2us+ pulse to activate TRIAC
    set(pins, 1)            # At 20kHz a pulse is 50us
    set(pins, 0)

    # 6. Close loop (Jump back to wait zx)
    jmp('waitzx')
    wrap()
# end def

# Setup the StateMachine at 20kHz (50us per instruction)
sm = rp2.StateMachine(0,
    dimmer,
    freq=20_000,
    in_base=zxpin,
    set_base=trpin
)
sm.active(1)

# At 60Hz the period is 8.33ms = 8,333us
# At 20kHz the each state machine step takes 50us
# Between the falling and rising edge there is a time window
# in which the new timeout/delay is set.
# The TRIAC needs a 2us pulse to switch on, so one instruction
# shall be enough.
# For an (almost) whole cycle of 8.3ms, the timeout must be
# set to (8300 - Δt - 20*50)/50 = 146
# where Δt is the gap between the zx edges. We assume it is
# zero since it is compensated by the 17cycle delay in the
# state machine for voltage stabilization.
while True:
    # delay = int(input('Delay: '))
    # sm.put(delay)
    # print(f'Delay: {delay}')
    # continue

    for power in range(0, 101):
        delay = 150 - int(150 * power / 100)
        sm.put(delay)
        print(f'Power: {power} | Delay: {delay}')
        sleep_ms(250)
    # end for
    for power in range(100, -1, -1):
        delay = 150 - int(150 * power / 100)
        sm.put(delay)
        print(f'Power: {power} | Delay: {delay}')
        sm.put(delay)
        sleep_ms(250)
    # end for
#end while
