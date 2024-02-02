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
int pdelay = 0;
int inc = 1;

// Prototypes
void turnLampOn(void);

/**
* Setup the Arduino
*/
void setup(void){
	// Setup interupt pin (input)
	pinMode(ZXPIN, INPUT);
	// digitalPinToInterrupt may not work, so we choose directly the
	// interrupt number. It is Zero for pin 2 on Arduino UNO
	// attachInterrupt(digitalPinToInterrupt(ZXPIN), zxhandle, RISING);
	attachInterrupt(0, zxhandle, RISING);
	// Setup output (triac) pin
	pinMode(TRIAC, OUTPUT);
	// Blink led on interrupt
	pinMode(13, OUTPUT);
	Serial.begin(9600);
}

void loop(){
	while (Serial.available() > 0){
		pdelay = Serial.parseInt();
		Serial.println(pdelay);
	}
}

void turnLampOn(){
	// Turn sentinel LED on
	digitalWrite(13, HIGH);
	// Send a 10us pulse to the TRIAC
	digitalWrite(TRIAC, HIGH);
	delayMicroseconds(20);
	digitalWrite(TRIAC, LOW);
}

void zxhandle(){
	flag = true;
	// TRIAC automatically shuts down on ZX
	digitalWrite(TRIAC, LOW);
	digitalWrite(13, LOW);

	delayMicroseconds(pdelay);

	if(pdelay > 0) turnLampOn();
}
