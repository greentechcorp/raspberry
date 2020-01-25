import time
import tof
import camera
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
 
#GPIO and Setup for tof distance sensor
# GPIO for Sensor 1 shutdown pin
sensor1_shutdown = 17
sensor1_address = 0x2B
# GPIO for Sensor 2 shutdown pin
sensor2_shutdown = 27
sensor2_address = 0x2D
# GPIO for Sensor 3 shutdown pin
sensor3_shutdown = 22
sensor3_address = 0x2F

tof1 = tof.tof_sensor(sensor1_shutdown, 0x2B)
tof2 = tof.tof_sensor(sensor2_shutdown, 0x2D)
tof3 = tof.tof_sensor(sensor3_shutdown, 0x2F)
tof_timing = tof1.get_timing()

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

def size():
    time.sleep(1)
    dist1 = tof1.get_distance(tof_timing)
    dist2 = tof2.get_distance(tof_timing)
    dist3 = tof3.get_distance(tof_timing)
    print("Sensor 1: ", dist1)
    print("Sensor 2: ", dist2)
    print("Sensor 3: ", dist3)


def objectFound():
    redLED()
    laser(0)
    print("There an object")
    print("The size is:")
    size()
    camera.take_picture()
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
