import time
import VL53L0X
import subprocess
import RPi.GPIO as GPIO

#box sizes
diameter = 120
totalDist = 150
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#GPIO and Setup for Pressuare Pad
pressurePad = 4
GPIO.setup(pressurePad,GPIO.IN)
 
#GPIO and Setup for LEDs
red = 6
green = 5
laser = 12

GPIO.setup(red,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)
GPIO.setup(laser,GPIO.OUT)

GPIO.output(red,GPIO.LOW)
GPIO.output(green,GPIO.HIGH)
GPIO.output(laser,GPIO.HIGH)
 
#GPIO and Setup for HC-SR04
GPIO_TRIGGER_1 = 18
GPIO_ECHO_1 = 23
GPIO_TRIGGER_2 = 17
GPIO_ECHO_2 = 22
 
GPIO.setup(GPIO_TRIGGER_1, GPIO.OUT)
GPIO.setup(GPIO_ECHO_1, GPIO.IN)
GPIO.setup(GPIO_TRIGGER_2, GPIO.OUT)
GPIO.setup(GPIO_ECHO_2, GPIO.IN)

# Create a VL53L0X object
tof = VL53L0X.VL53L0X()

# Start ranging
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

def laser(x):
    if (x==1):
        GPIO.output(12,GPIO.HIGH)
    else:
        GPIO.output(12,GPIO.LOW)

def redLED():
    GPIO.output(red,GPIO.HIGH)
    GPIO.output(green,GPIO.LOW)

def greenLED():
    GPIO.output(green,GPIO.HIGH)
    GPIO.output(red,GPIO.LOW)

def Blink():
    greenLED()
    time.sleep(0.1)
    redLED()
    time.sleep(0.1)
    greenLED()
    time.sleep(0.1)
    redLED()
    time.sleep(0.1)
    greenLED()


def distanceHCSR04(trigger,echo):
    GPIO.output(trigger, True)
 
    time.sleep(0.00001)
    GPIO.output(trigger, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    while GPIO.input(echo) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance = int((TimeElapsed * 343000) / 2)
 
    return distance

def size():
    time.sleep(1)
    dist1 = distanceHCSR04(GPIO_TRIGGER_1,GPIO_ECHO_1)
    dist2 = distanceHCSR04(GPIO_TRIGGER_2,GPIO_ECHO_2)
    dist3 = tof.get_distance()
    print ("Sensor 1: ", dist1)
    print ("Sensor 2: ", dist2)
    print ("Sensor 3: ", dist3)


def objectFound():
    redLED()
    laser(0)
    print("There an object")
    print("The size is:")
    size()
    cam = subprocess.Popen('./pic.sh')
    cam.wait()
    laser(1)
    greenLED()

def objectGone():
    print ("The object is gone")
    Blink()
    pressure()


def pressure():
    input = GPIO.input(pressurePad)
    time.sleep(0.1)
    if (input):
        objectFound()
        while (input):
            greenLED()
            input = GPIO.input(pressurePad)
            time.sleep(0.2)
            redLED()
            time.sleep(0.2)
        objectGone()


while True:
    pressure()
    time.sleep(0.2)
