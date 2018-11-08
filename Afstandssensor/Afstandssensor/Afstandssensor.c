#include <avr/io.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include <util/delay.h>
#include <avr/interrupt.h>
#include <string.h>

#define UBBRVAL 51
#define HIGH 0xff
#define LOW 0x00

volatile char echoDone = 0;
uint32_t countTimer0 = 0;


//Serialisering
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

//transmit to serial
void transmit(uint8_t data)
{
	loop_until_bit_is_set(UCSR0A, UDRE0);
	UDR0 = data;
}

//send sr04 signal and calculate distance
void SR04Signal(){
		
	
	float distance = 0.00;
	
	//echoDone is een boolean die checkt of de echo klaar is
	//Als de echo pas klaar is mag ermee worden gerekend
	echoDone = 0;
	
	//Timer0 counter wordt gereset
	countTimer0 = 0;
	
	
	//send pulse to trigger
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
	
	uart_init();
    SCH_Init_T1();
	SCH_Add_Task(SR04Signal,0,50);
	SCH_Start();
	while (1)
	{
		SCH_Dispatch_Tasks();
	}	  
	return 0;
}
