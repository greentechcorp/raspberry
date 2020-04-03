import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)

prev_input = 0

    
while True:
    input = GPIO.input(4)
    print (input)