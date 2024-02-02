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

// Power factor
volatile float pfactor = 0;

// Timer 1 overflow for 1 sec at 16MHz with 1024 prescaler
volatile int overflow = 49910;

// Buffer to write in serial
char sbuffer[40];
char fbuffer[10];

/**
* Setup the Arduino
*/
void setup(void){
	// Initialize timer 1
	noInterrupts();
	TCCR1A = 0;
	TCCR1B = 0;
	// Set prescaler to 1024
	TCCR1B |= (1 << CS10)|(1 << CS12);
	// Set overflow value
	TCNT1 = overflow;
	// Enable timer interrupt
	TIMSK1 |= (1 << TOIE1);

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

	// Enable interrupts
	interrupts();

	// Setup Serial port
	Serial.begin(9600);
}

void loop(){
	// delayMicroseconds(10);
	delay(100);


	dtostrf(100 * pfactor, 3, 1, fbuffer);
	sprintf(sbuffer, "Power factor: %s ", fbuffer);
	Serial.print(sbuffer);

	dtostrf(8.3 * (1-pfactor), 4, 2, fbuffer);
	sprintf(sbuffer, "Delay: %sms", fbuffer);
	Serial.println(sbuffer);

	// Calculate phase linearly (incorrect approach):
	// Each crest lasts about 8.3ms at 120Hz
	// ON time is crest length × (1 - power-factor / 100)
	// Overflow = 65535 - (16MHz × time) / Prescaler
	// Overflow = 65535 - (16MHz × (8.3ms × (1-pfactor / 100)) ) / Prescaler
	// overflow = 65535 - 16MHz × 8.3ms × (1-pfactor / 100) / 1024;
	// overflow = 65535 - 16MHz × 1s/120 × (1-pfactor) / 102400;
	// overflow = 65535 - 16×10⁶ × (1-pfactor) / 122880;
	// overflow = 65535 - 130.2 * (1-pfactor);
	overflow = 65535 - 130.2 * (1-pfactor);

	pfactor+= 0.01;
	// Increment/reset power factor
	if(pfactor > 1) pfactor = 0;

}

void zxhandle(){
	flag = true;
	// Turn off lamp
	digitalWrite(TRIAC, LOW);
		TCNT1 = overflow;
	}
}

ISR(TIMER1_OVF_vect){
	// Timer to 1 second
	TCNT1 = 49910;
	// Turn on lamp
	digitalWrite(TRIAC, HIGH);
	digitalWrite(13, HIGH);
}

