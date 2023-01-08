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
#define VAREF 2.7273
#define I2C_SLAVE_ADDR 0x0A
#define BOARD_LED 13

// Global variables
float temperature = 0;

// Prototypes
void i2c_received_handler(int count);
void i2c_request_handler(int count);
float read_temp(void);
float read_avg_temp(int count);

/**
* Setup the Arduino
*/
void setup(void){
	// Configure ADC to use voltage reference from AREF pin (external)
	analogReference(EXTERNAL);
	// Set ADC resolution to 10 bits
	// analogReadResolution(10)

	// Configure I2C to run in slave mode with the defined address
	Wire.begin(I2C_SLAVE_ADDR);
	// Configure the handler for received I2C data
	Wire.onReceive(i2c_received_handler);
	// Configure the handler for request of data via I2C
	Wire.onRequest(i2c_request_handler);

	// Setup the serial port to operate at 56.6kbps
	Serial.begin(56600);

	// Setup board led
	pinMode(BOARD_LED, OUTPUT);

}

/**
* Handles data requests received via the I2C bus
* It will immediately send the temperature read as a float value
*/
void i2c_request_handler(){
	Wire.write((byte*) &temperature, sizeof(float));
}

/**
* Handles received data via the I2C bus.
* Data is forwarded to the Serial port and makes the board led blink
*/
void i2c_received_handler(int count){
	char received = 0;
	while (Wire.available()){
		received = (char)Wire.read();
		digitalWrite(BOARD_LED, received ? HIGH : LOW);
		Serial.println(received);
	}

}

/**
* Reads temperature in C from the ADC
*/
float read_temp(void){
	// The actual temperature
	int vplus  = analogRead(0);
	// The reference temperature value, i.e. 0°C
	int vminus = analogRead(1);
	// Calculate the difference. when V+ is smaller than V- we have negative temp
	int vdiff = vplus - vminus;
	// Temp = vdiff * VAREF / (1024 * 0.01)
	return vdiff * VAREF / 10.24f;
}

void loop(){
	temperature = read_temp();
	delay(100);
}
