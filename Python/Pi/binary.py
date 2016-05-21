import RPi.GPIO as GPIO
import time
import threading
BITS=8
GPIO.setmode(GPIO.BCM)
#i know the anodes and cathodes are the wrong way around, please ignore
cathodes_led=(8,7)
anodes_led=(12,16,20,21)
buttons=(9,11,0,5,6,13,19,26)
segments=(2,3,4,17,27,22,10)
anodes_seg=(18,23,24)

powers=[2**n for n in range (BITS-1,-1,-1)] #descending powers of 2
bigbutton=25
bits=[False for b in range(BITS)]

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
digits=[0,8,0]



def encode(x): #sloppy way of getting the number for each digit
	digits[0]=(x%1000)//100
	digits[1]=(x%100)//10
	digits[2]=(x%10)//1

def writebits(val):
	x=val
	print('writing', val)
	for i, pwr in enumerate(powers): #convert the number to bits
		if x-pwr >= 0:
			x-=pwr
			bits[i]=True
		else:
			bits[i]=False

def readbits():
	x=0
	for bit, pwr in zip(bits, powers):
			x+=bit*pwr
	print('read', x)
	return x
	
def setbit(channel):
	global value
	print('set bit')
	_input=buttons.index(channel)
	print(_input, channel)
	bits[_input]=not bits[_input] #reverse bit
	value=readbits()
	encode(value)

def increment(channel):
	global value
	print('incrementing')
	value+=1
	value%=2**BITS
	writebits(value)
	encode(value)

def segment_modulate(): #runs in separate thread
	while(1):
		for anode, digit in zip(anodes_seg, digits):
			for seg, out in zip(segments, layouts[digit]):
				GPIO.output(seg, out)
			GPIO.output(anode, False) #this is not really PWM but it works
			time.sleep(0.001)
			GPIO.output(anode, True)

def led_modulate(): #this function never actually runs cause i put its contents in the main thread
	while(1):
		for i, cathode in enumerate(cathodes_led):
			for anode, out in zip(anodes_led, [not bit for bit in bits[4*i:4*i+4]]):
				GPIO.output(anode, out)
			GPIO.output(cathode, True)
			time.sleep(0.002)
			GPIO.output(cathode, False)

#set up every single port
for seg in segments:
	GPIO.setup(seg, GPIO.OUT)
	GPIO.output(seg, True)
for anode in anodes_seg:
	GPIO.setup(anode, GPIO.OUT)
	GPIO.output(anode, True)
for cathode in cathodes_led:
	GPIO.setup(cathode, GPIO.OUT)
	GPIO.output(cathode, True)
for anode in anodes_led:
	GPIO.setup(anode, GPIO.OUT)
	GPIO.output(anode, False)
for btn in buttons:
	GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #the inputs are pull down so that they detect a HIGH voltage
	print(GPIO.input(btn))
	GPIO.add_event_detect(btn, GPIO.RISING, callback=setbit, bouncetime=500) #call setbit function when rising edge (LOW to HIGH) detected for each button

GPIO.setup(bigbutton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(bigbutton, GPIO.RISING, callback=increment, bouncetime=500)
value = 0
writebits(0)

segment_thread = threading.Thread(target=segment_modulate)
led_thread = threading.Thread(target=led_modulate)
segment_thread.start()
#led_thread.start()
encode(value)
try:
	while(1):
		for i, cathode in enumerate(cathodes_led):
			for anode, out in zip(anodes_led, [not bit for bit in bits[4*i:4*i+4]]):
				GPIO.output(anode, out)
			GPIO.output(cathode, True)
			time.sleep(0.002)
			GPIO.output(cathode, False)
except KeyboardInterrupt:
	GPIO.cleanup()
	
	 
