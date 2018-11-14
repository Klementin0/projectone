/*
MISSEND: Setup ldr en temp - hiermee dus ook de check
		ledcheck() doet het niet, recieve moet worden gefixt

VOLGORDE BREADBOARD PLUSLIJN temp > licht > afstand
Dit is omdat temp en licht zich anders gedragen met verschillende volt
als dit verkeerd wordt opgezet kunnen waardes afwijken
Omdat temp het meest precies wordt gemeten en licht nog anders reageert op kiezen we
voor deze opzet. Het maken en meten van de afstandssignalen hebben hier geen last van

-------------------------------------------------------------------------------------

ldr & temp36
UART code source: homework Assembly & C week 4 (partly blackboard)
ADC code source: https://sites.google.com/site/qeewiki/books/avr-guide/analog-input
This is the basic code to continuously read values from the LDR04 sensor
and transmit this value as int value over a serial connection using UART.

Temp:
VCC: 5V
Pin: analog in A0
GND: Gnd
(voor pinschema zie https://www.analog.com/media/en/technical-documentation/data-sheets/TMP35_36_37.pdf)

LDR04:
1 zijde van de LDR04 verbinden met 5V. De andere zijde met zowel analog in A1 en via een 10kOhm weerstand met de Gnd
(parallel zodat er een spanningsdeler gecreeerd wordt).

Created: 6-11-2018 14:34:25
Author: Kevin

-------------------------------------------------------------------------------------

Afstandsensor & merge
Created by: Youri van de Geer - 372724
Code from - blackboard and references to forums
8/11/2018

Accuracy: full CM

PB0 = echo
PB1 = trigger
GRND = GRND
V5 = VCC

voor test -> PD4 - led - weerstand - ground

BAUDRATE = 19200
PORT = PORT (COM3 on my device)
Display = uint8_t
No parity - 8 Data bits - 1 stop bit
*/
#include <avr/io.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include <util/delay.h>
#include <avr/interrupt.h>
#include <string.h>


#define UBBRVAL 51

volatile char echoDone = 0;
uint32_t countTimer0 = 0;
float avgtemp = 0.0;
uint8_t light = 0;
uint8_t currentdistance;
uint8_t mode = 1;

char input;

//serialisering
void uart_init() {
	// set the baud rate
	UBRR0H = 19200;
	UBRR0L = UBBRVAL;
	// disable U2X mode
	UCSR0A = 0;
	// enable transmitter and receiver
	UCSR0B = _BV(TXEN0)|_BV(RXEN0);
	// set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
}
//transmitten naar Realterm/Putty/Centrale
void transmit(uint8_t data)
{
	// wait for an empty transmit buffer
	// UDRE is set when transmit buffer is empty
	loop_until_bit_is_set(UCSR0A, UDRE0);
	// send the data
	UDR0 = data;
}

unsigned char receive(void)
{
	/* Wait for data to be received */
	while ( !(UCSR0A & (1<<RXC0)) );
	/* Get and return received data from buffer */
	return UDR0;
}

int message_incoming(void)
{
	if((UCSR0A & (1<<RXC0))){
		return 1;
	} else {
		return 0;
	}
}

void input_handler(){
	if(message_incoming()){
		input = receive();
		
		if (input = 49){
			if(mode = 0){
				mode = 1;
			}
			if (mode = 1)
			{
				mode = 0;
			}
		}
		
	}

}

//AnalogRead
int ADCsingleREAD(uint8_t adctouse)
{
	int ADCval;

	ADMUX = adctouse;         // use #1 ADC
	ADMUX |= (1 << REFS0);    // use AVcc as the reference
	ADMUX &= ~(1 << ADLAR);   // clear for 10 bit resolution

	ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);    // 128 prescale for 16Mhz
	ADCSRA |= (1 << ADEN);    // Enable the ADC

	ADCSRA |= (1 << ADSC);    // Start the ADC conversion

	while(ADCSRA & (1 << ADSC));      // Thanks T, this line waits for the ADC to finish


	ADCval = ADCL;
		ADCval = (ADCH << 8) + ADCval;    // ADCH is read so ADC can be updated again

	return ADCval;
}
//Temp sensor
float readTemp()
{
	int ADCvalue;	//int variabele ADCValue aanmaken
	ADCvalue = ADCsingleREAD(0);	//Lees de ADC uit voor pin 0 en sla deze op in ADCValue
    float temperatuur = 0.00;	//Float variabele aanmaken voor het berekenen van- en opslaan van temperatuur
	temperatuur = ((ADCvalue * (5000.0/1024.0)) - 500.0) /10.0;	//Temperatuur berekenen uit ADCValue
	return temperatuur;	//return temperatuur in float formaat
}
//lichtsensor
void readLDR()
{
	int ADCvalue;	//int variabele ADCValue aanmaken
	ADCvalue = ADCsingleREAD(1);	//Lees de ADC uit voor pin 1 en sla deze op in ADCValue
	if (ADCvalue <= 150) //maak booleaanse expressie met licht(1) of donker(0) als uitkomst
	{
		light = 0;	//stel variabele light in op 0(donker)
	}
	if (ADCvalue > 150)
	{
		light = 1;	//stel variabele light in op 1(licht)
	}
}

void calculateAvgTemp()
{
	int a;
	float totaal = 0.0;
	for(a = 0; a <10; a++)
	{
		totaal += readTemp();
	}	
	avgtemp = totaal / 10.0;
}

//zend sr04 signaal en reken hiermee
void SR04Signal(){


	float distance = 0.00;

	//echoDone is een boolean die checkt of de echo klaar is
	//Als de echo pas klaar is mag ermee worden gerekend
	echoDone = 0;

	//Timer0 counter wordt gereset
	countTimer0 = 0;


	//pulse sturen naar de trigger
	PORTB = 0x00;
	_delay_ms(2);
	PORTB = 0xff;
	_delay_us(10);
	PORTB = 0x00;

	//check of echo weer low is
	while (!echoDone);

	//berekening afstand
	distance = countTimer0/16E6;
	distance = 17013.0*distance;

	//verzenden naar serial
	if(distance <= 6){currentdistance = 5;}
	else if(distance > 160){currentdistance = 161;}
	else{currentdistance = round(distance);}

}

void transmitData()
{
	transmit(avgtemp);
	_delay_ms(1);
	transmit(light);
	_delay_ms(1);
	transmit(currentdistance);
	_delay_ms(1);
}

void autoMode()
{
	if (mode == 1)
	{
		if (currentdistance == 5)
		{
			if (light == 1)
			{
				if (avgtemp >= 10.0)
				{
					rollOut();
				}
			}
		}
		else if (currentdistance == 161)
		{
			if (light == 0)
			{
				rollIn();
			}
			else if (avgtemp < 10.0)
			{
				rollIn();
			}
		}
	}
}

void rollOut()
{
	uint8_t status = PORTD;
	if (status &= 0b00000100)
	{
		PORTD = PORTD<<1;
		_delay_ms(3000);
		PORTD = PORTD<<1;
	}
}

void rollIn()
{
	uint8_t status = PORTD;
	if (status &= 0b00010000)
	{
		PORTD = PORTD>>1       ;
		_delay_ms(3000);
		PORTD = PORTD>>1;
	}
}

//overflow interrupt op timer 0
ISR(TIMER0_OVF_vect){
	countTimer0 += 255;
}
//Interrupt voor PCINT0 ECHO PIN(pinb0)
ISR (PCINT0_vect){
	//als echo pin aan gaat de timer starten
	if (PINB != 0x00){

		TCCR0B |= (1<<CS00);
		TIMSK0 |= 1<<TOIE0;

	}//als echo pin uit gaat de timer stoppen en waarden aan countTimer0 meegeven
	else{
		
		TCCR0B &= ~(1<<CS00);
		countTimer0 += TCNT0;
		TCNT0 = 0;
		//echoDone flag op 1 zetten zodat ermee kan worden gerekend
		echoDone = 1;

	}
}

int main() {

	//Poort init
	DDRB = 0xfe;
	DDRD = 0xff;
	PORTD = 0b00000100;

	//PCINT0 init
	PCICR |= (1 << PCIE0);
	PCMSK0 |= (1<< PCINT0);
	
	uart_init();//init serialisering

	//scheduler
	SCH_Init_T1();
	
	SCH_Add_Task(calculateAvgTemp,0,4000);
	SCH_Add_Task(readLDR,0,3000);
	SCH_Add_Task(SR04Signal,0,50);
	SCH_Add_Task(transmitData,0,60);
	SCH_Add_Task(input_handler,0,1);
	SCH_Add_Task(autoMode,200,1000);
	
	SCH_Start();

	//run scheduler
	while(1) {
		SCH_Dispatch_Tasks();
	}

	return 0;
}
