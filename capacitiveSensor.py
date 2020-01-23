import time
import RPi.GPIO as GPIO

GPIOpin = -1

def initialInductive(pin):
  global GPIOpin 
  GPIOpin = pin
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(GPIOpin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  print("Finished Initiation")
  print(GPIOpin)

def detectMetal():
  if(GPIOpin != -1):
    state = GPIO.input(GPIOpin)
    if state:
	  print("Object Detected")
    else:
      print("No Object")
  else:
    print("Please Initialize Input Pin")
    
pin = 20
initialInductive(pin)
while True:
    detectMetal()
    time.sleep(0.2)
