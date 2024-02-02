/*
* arduino-test-zx.cpp
*
* Author:  Mauricio Matamoros
* Date:    2020.03.01
* License: MIT
*
* Prints the number of times the AC phase of the power
* line crossed zero (neutral) on the Serial port
*
*/

// Digital 2 is Pin 2 in UNO
#define ZXPIN 2
// Digital 3 is Pin 3 in UNO
#define TRIAC 3

// Globals
volatile bool flag = false;

// Zero-cross count
int count = 0;

// 16MHz → 16×10⁶ / 1024 = 15.625kHz timer or 1 tick every 64us
// Overflow = 65535 - (16MHz × time) / Prescaler
// Overflow = 65535 - (16MHz × 1s) / 1024
// Overflow = 65535 - 15625 = 49910
int overflow = 49910;

// Buffer to write in serial
char buffer[40];



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
	// Output to blink led on interrupt
	pinMode(13, OUTPUT);

	// Enable interrupts
	interrupts();

	// Setup Serial port
	Serial.begin(9600);
}

void loop(){
	if(!flag){
		// Slack until next interrupt
		delayMicroseconds(10);
		return;
	}
	// Reset flag
	flag = !flag;
	digitalWrite(13, LOW);
	// Print zx count. Must be 2x the AC frequency
	sprintf(buffer, "Count: %d", count);
	count = 0;
	Serial.println(buffer);
}

void zxhandle(){
	digitalWrite(13, HIGH);
	++count;
}

ISR(TIMER1_OVF_vect){
	TCNT1 = overflow;
	flag = true;
}
