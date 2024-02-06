# ## #############################################################
#
# src/pico-code-adc.py
#
# Author: Mauricio Matamoros
# Date:
#
# ## ############################################################
from machine import ADC          # Board Analogic-to-Digital Converter
from utime import sleep_ms       # Delay function in milliseconds

VAREF = 2.72

def setup():
    '''
        Setup the Pico
    '''
    adcm = machine.ADC(0)         # Init ADC0
    adcp = machine.ADC(1)         # Init ADC1
# end def


def read_temp():
    '''
        Reads temperature in C from the ADC
    '''
    # The actual temperature
    vplus  = adcp.read_u16()
    # The reference temperature value, i.e. 0°C
    vminus = adcm.read_u16()
    # Calculate the difference. when V+ is smaller than V- we have negative temp
    vdiff  = vplus - vminus
    # Now, we need to convert values to the ADC resolution, AKA 2.72V/4096
    # We also know that 1°C = 0.01V so we can multiply by 2.72V / (0.01V/°C) = 272°C
    # to get °C instead of V. Analogously we can multiply VAREF by 100 but
    # since we will divide per 4096, it suffice with dividing by 40.96
    temp = vdiff * VAREF / 40.96
# end def


def read_avg_temp(count=10):
    '''
        Gets the average of N temperature reads
    '''
    avgtemp = 0
    for i in range(count):
        avgtemp += read_temp()
    return avgtemp / count
# end def


def main():
    while(True):                      # Repeat forever
        temp = read_avg_temp()        # Fetch temperature
        print(f'Temp: {temp:0.2f}°C') # Print temperature
        sleep_ms(1000)                # Wait for 1000ms
#end def

if __name__ == '__main__':
    main()
