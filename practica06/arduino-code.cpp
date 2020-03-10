/*
* arduino-code.cpp
*
* Author:  Mauricio Matamoros
* Date:    2020.03.01
* License: MIT
*
* Reads temperature from the pins A0 (Vout+ )and A1 (Vout-) using a LM35
* with a voltage divider to supply 2.7V to AREF
*
*/

#define VAREF 2.7273

// Prototypes
float read_temp(void);
float read_avg_temp(int count);

/**
* Setup the Arduino
*/
void setup(void){
	// Configure ADC to use voltage reference from AREF pin (external)
	analogReference(EXTERNAL);
	// Set ADC resolution to 10 bits
	// analogReadResolution(10);

	// Setup the serial port to operate at 56.6kbps
	Serial.begin(9600);
	pinMode(13, OUTPUT);
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
	/* Now, we need to convert values to the ADC resolution, AKA 2.72V/1024
	*  We also know that 1C = 0.01V so we can multiply by 2.72V / (0.01V/°C) = 272°C
	*  to get C instead of V. Analogously we can multiply VAREF by 100 but
	*  since we will divide per 1024, it suffice with dividing by 10.24
	*/
	float temp = vdiff * VAREF / 10.24f;
	return temp;
}

/**
* Gets the average of N temperature reads
*/
float read_avg_temp(int count){
	float avgtemp = 0;
	for(int i = 0; i < count; ++i)
		avgtemp += read_temp();
	return avgtemp / count;
}

void loop(){
	float temp = read_avg_temp(5);
	Serial.print((int)temp);
	Serial.print(".");
	Serial.println((int)(10 * temp) % 10);
	digitalWrite(13, HIGH);
	delay(5);
	digitalWrite(13, LOW);
	delay(5);
}
