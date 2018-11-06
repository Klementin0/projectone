/*
 * ldr.c
 * UART code source: homework Assembly & C week 4
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
volatile uint8_t ADCvalue;    // Global variable, set to volatile if used with ISR

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
//EINDE VOORBEELDCODE BLACKBOARD
char receive(void) {
	loop_until_bit_is_set(UCSR0A, RXC0); //wacht totdat RXC0 is set en enable transmitter&reciever
	return UDR0; // return waarde van USART I/O Data Register
}

void sensorinit(void)
{
	ADMUX = 0;                // use ADC0
	ADMUX |= (1 << REFS0);    // use AVcc as the reference
	ADMUX |= (1 << ADLAR);    // Right adjust for 8 bit resolution

	ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // 128 prescale for 16Mhz
	ADCSRA |= (1 << ADATE);   // Set ADC Auto Trigger Enable
	
	ADCSRB = 0;               // 0 for free running mode

	ADCSRA |= (1 << ADEN);    // Enable the ADC
	ADCSRA |= (1 << ADIE);    // Enable Interrupts

	ADCSRA |= (1 << ADSC);    // Start the ADC conversion

	sei();    // Thanks N, forgot this the first time =P
}

ISR(ADC_vect)
{
	ADCvalue = ADCH;          // only need to read the high value for 8 bit
	// REMEMBER: once ADCH is read the ADC will update
	
	// if you need the value of ADCH in multiple spots, read it into a register
	// and use the register and not the ADCH
	transmit(ADCvalue);
	_delay_ms(1000);
}

int main() {
	uart_init();//initialisatie uart
	sensorinit();//initialisatie sensoren
	_delay_ms(1000);//delay voor begin while loop
	while(1) {
		
	}
	return 0;
}