/*
* arduino-code.cpp
*
* Author:  Mauricio Matamoros
* Date:    2020.03.01
* License: MIT
*
* Reads temperature from the pins A0 (Vout+ )and A1 (Vout-) using a LM35
* with a voltage divider to supply 2.7V to AREF, and sends it via I2C bus
*
*/
#include <Wire.h>

// Constants
#define I2C_SLAVE_ADDR 0x0A
#define BOARD_LED 13

/**
* Setup the Arduino
*/
void setup(void){
	// Configure I2C to run in slave mode with the defined address
	Wire.begin(I2C_SLAVE_ADDR);
	// Configure the handler for request of data via I2C
	Wire.onRequest(i2c_request_handler);
	// Setup board led
	pinMode(BOARD_LED, OUTPUT);
}

/**
* Handles data requests received via the I2C bus
* It will immediately send the temperature read as a float value
*/
void i2c_request_handler(){
	byte temperature = 20;
	Wire.write((byte*) &temperature, 1);
	// float temperature = 20.0f;
	// Wire.write((byte*) &temperature, 4);
}

/**
* Handles received data via the I2C bus.
* Data is forwarded to the Serial port and makes the board led blink
*/
void i2c_received_handler(int count){
	while (Wire.available()){
		Wire.read();
		digitalWrite(BOARD_LED, HIGH);
	}
	digitalWrite(BOARD_LED, LOW);
}

void loop(){
	delay(100);
}
