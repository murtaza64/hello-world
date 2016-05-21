import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
toggle=False
print('start')
while(1):
	if GPIO.read(21): toggle=!toggle
	if toggle:
		GPIO.output(17, True)
	else:
		GPIO.output(17, False)
	time.sleep(1)
