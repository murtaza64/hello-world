import RPi.GPIO as GPIO
import time
import sys
GPIO.setmode(GPIO.BCM)
segments=(2,3,4,17,27,22,10)
anodes=(5,6,13)
layouts=(
	(1,1,1,1,1,1,0),
	(0,1,1,0,0,0,0),
	(1,1,0,1,1,0,1),
	(1,1,1,1,0,0,1),
	(0,1,1,0,0,1,1),
	(1,0,1,1,0,1,1),
	(1,0,1,1,1,1,1),
	(1,1,1,0,0,0,0),
	(1,1,1,1,1,1,1),
	(1,1,1,0,0,1,1)
	
	)
digits=[0,0,0]
for seg in segments:
	GPIO.setup(seg, GPIO.OUT)
	GPIO.output(seg, True)
for anode in anodes:
	GPIO.setup(anode, GPIO.OUT)
	GPIO.output(anode, True)
def encode(x):
	digits[0]=(x%1000)//100
	digits[1]=(x%100)//10
	digits[2]=(x%10)//1
while(1):
	encode(int(sys.argv[1]))
	for anode, digit in zip(anodes, digits):
		for seg, out in zip(segments, layouts[digit]):
			GPIO.output(seg, out)
		GPIO.output(anode, False)
		time.sleep(0.003)
		GPIO.output(anode, True)
		
