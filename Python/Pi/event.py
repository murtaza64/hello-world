import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(19, GPIO.IN)
off=1
GPIO.output(12, True)
def update(channel):
	print(channel)
	global off
	if off:
		GPIO.output(12, False)
	else:
		GPIO.output(12, True)
	off=not off
GPIO.add_event_detect(19, GPIO.RISING, callback=update, bouncetime=500)

while True:
	continue
