import RPi.GPIO as GPIO
import time
import threading
BITS=4
GPIO.setmode(GPIO.BCM)
cathodes_led=(8,7)
anodes_led=(12,16,20,21)
buttons=(9,11,0,5,6,13,19,26)
segments=(2,3,4,17,27,22,10)
anodes_seg=(18,23,24)
bits=[True, True, True, True, False, False, False, False]
for seg in segments:
	GPIO.setup(seg, GPIO.OUT)
	GPIO.output(seg, True)
for anode in anodes_seg:
	GPIO.setup(anode, GPIO.OUT)
	GPIO.output(anode, True)
for cathode in cathodes_led:
	GPIO.setup(cathode, GPIO.OUT)
	GPIO.output(cathode, False)
for anode in anodes_led:
	GPIO.setup(anode, GPIO.OUT)
	GPIO.output(anode, False)
for btn in buttons:
	GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	print(GPIO.input(btn))

while(1):
	for i, cathode in enumerate(cathodes_led):
		for anode, out in zip(anodes_led, [not bit for bit in bits[4*i:4*i+4]]):
			GPIO.output(anode, out)
		GPIO.output(cathode, True)
		time.sleep(0.002)
		GPIO.output(cathode, False)
