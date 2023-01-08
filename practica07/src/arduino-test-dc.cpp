/*
* arduino-test-dc.cpp
*
* Author:  Mauricio Matamoros
* Date:    2020.03.01
* License: MIT
*
* Controls the power output of a resistive load using
* zero-cross detection and a TRIAC. Code for Arduino UNO
*
*/

// Digital 2 is Pin 2 in UNO
#define ZXPIN 2
// Digital 3 is Pin 3 in UNO
#define TRIAC 3

// Globals
volatile bool flag = false;
int pfactor = 0;

// Prototypes
float read_temp(void);
float read_avg_temp(int count);

/**
* Setup the Arduino
*/
void setup(void){
	// Setup interupt pin (input)
	pinMode(ZXPIN, INPUT);
	attachInterrupt(digitalPinToInterrupt(ZXPIN), zxhandle, RISING);
	// Setup output (triac) pin
	pinMode(TRIAC, OUTPUT);
	// Blink led on interrupt
	pinMode(13, OUTPUT);
}

void loop(){
	if(!flag){
		// Slack until next interrupt
		delayMicroseconds(10);
		return;
	}
	// Reset flag
	flag = !flag;
	// Keep power on for pfactor us
	delayMicroseconds(pfactor);
	// Disable power
	digitalWrite( 3, LOW);
	digitalWrite(13, LOW);
	// Increment/reset power factor
	pfactor+= 10
	if(pfactor > 8000) pfactor = 0;
}

void zxhandle(){
	flag = true;
	// Enable power
	digitalWrite( 3, HIGH);
	digitalWrite(13, HIGH);
}
