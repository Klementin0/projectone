/*
MISSEND: Setup ldr en temp - hiermee dus ook de check

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

//AnalogRead
int ADCsingleREAD(uint8_t adctouse)
{
	int ADCval;

	ADMUX = adctouse;         // use #1 ADC
	ADMUX |= (1 << REFS0);    // use AVcc as the reference
	ADMUX &= ~(1 << ADLAR);   // clear for 10 bit resolution
	
	ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);    // 128 prescale for 8Mhz
	ADCSRA |= (1 << ADEN);    // Enable the ADC

	ADCSRA |= (1 << ADSC);    // Start the ADC conversion

	while(ADCSRA & (1 << ADSC));      // Thanks T, this line waits for the ADC to finish


	ADCval = ADCL;
		ADCval = (ADCH << 8) + ADCval;    // ADCH is read so ADC can be updated again

	return ADCval;
}
//Temp sensor
int readTemp()
{
	int ADCvalue;
	ADCvalue = ADCsingleREAD(0);
    float temperatuur = 0.00;
	temperatuur = ((ADCvalue * (5000.0/1024.0)) - 500.0) /10.0;
	transmit(1);
	transmit(temperatuur);
}
//lichtsensor
int readLDR()
{
	int ADCvalue;
	ADCvalue = ADCsingleREAD(1);
	transmit(2);	
	transmit(ADCvalue);
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
	transmit(distance);
}

//overflow interrupt op timer 0
ISR(TIMER0_OVF_vect){
	countTimer0 += 255;
}
//Interrupt voor PCINT0 ECHO PIN(pinb0)
ISR (PCINT0_vect){
	//als echo pin aan gaat de timer starten
	if (PINB != 0x00){

		PORTD = 0xff;
		TCCR0B |= (1<<CS00);
		TIMSK0 |= 1<<TOIE0;

	}//als echo pin uit gaat de timer stoppen en waarden aan countTimer0 meegeven
	else{
		PORTD = 0x00;
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
		
	//PCINT0 init
	PCICR |= (1 << PCIE0);
	PCMSK0 |= (1<< PCINT0);
	
	uart_init();//init serialisering
	
	//scheduler
	SCH_Init_T1();
	SCH_Add_Task(readTemp,0,300);
	SCH_Add_Task(readLDR,100,300);
	SCH_Add_Task(SR04Signal,200,300);
	SCH_Start();
	
	//run scheduler
	while(1) {
		SCH_Dispatch_Tasks();
	}
	
	return 0;
}