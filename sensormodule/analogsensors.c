/*
 * ldr.c
 * UART code source: homework Assembly & C week 4 (partly blackboard)
 * ADC code source: https://sites.google.com/site/qeewiki/books/avr-guide/analog-input
 * This is the basic code to continuously read values from the LDR04 sensor 
 * and transmit this value as int value over a serial connection using UART.
 * Created: 6-11-2018 14:34:25
 *  Author: Kevin
 */ 

#include <avr/io.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include <util/delay.h>
#include <avr/interrupt.h>
//BEGIN VOORBEELDCODE BLACKBOARD
// output on USB = PD1 = board pin 1
// datasheet p.190; F_OSC = 16 MHz & baud rate = 19.200
#define UBBRVAL 51
int ADCvalue;

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
void transmit(uint8_t data)
{
	// wait for an empty transmit buffer
	// UDRE is set when transmit buffer is empty
	loop_until_bit_is_set(UCSR0A, UDRE0);
	// send the data
	UDR0 = data;
}

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

int readTemp()
{
	ADCvalue = ADCsingleREAD(0);
	transmit(ADCvalue);
}

int readLDR()
{
	ADCvalue = ADCsingleREAD(1);
	transmit(ADCvalue);
}

int main() {
	uart_init();//initialisatie uart
	_delay_ms(1000);//delay voor begin while loop
	SCH_Init_T1();
	SCH_Add_Task(readTemp,0,200);
	SCH_Add_Task(readLDR,100,200);
	SCH_Start();
	while(1) {
		SCH_Dispatch_Tasks();
	}
	return 0;
}