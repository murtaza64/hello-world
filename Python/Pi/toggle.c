#include <wiringPi.h>
#include <stdio.h>
int main(void){
	wiringPiSetup();
	pinMode(0, OUTPUT);
	pinMode(21, INPUT);
	int on = 0;
	for (;;){
		printf("cycle");
		if (!digitalRead(21)){
			on = 1-on;
			printf("on");
		}
		if (on){
			digitalWrite(0, HIGH);
		} else {
			digitalWrite(0, LOW);
		}
	}
	return 0;
}
