import time
import tof
import camera
import materialSensor
import RPi.GPIO as GPIO

file = open("data.csv", "a")

#box sizes
diameter = 120
totalDist = 150
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#GPIO and Setup for LEDs
red = 14
green = 5
laserPin = 26

GPIO.setup(red,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)
GPIO.setup(laserPin,GPIO.OUT)

GPIO.output(red,GPIO.LOW)
GPIO.output(green,GPIO.HIGH)
GPIO.output(laserPin,GPIO.LOW)
 
#GPIO and Setup for tof distance sensor
# GPIO for Sensor 1 shutdown pin
sensor1_shutdown = 6
sensor1_address = 0x2B
# GPIO for Sensor 2 shutdown pin
sensor2_shutdown = 13
sensor2_address = 0x2D
# GPIO for Sensor 3 shutdown pin
sensor3_shutdown = 19
sensor3_address = 0x2F

tof1 = tof.tof_sensor(sensor1_shutdown, 0x2B)
tof2 = tof.tof_sensor(sensor2_shutdown, 0x2D)
tof3 = tof.tof_sensor(sensor3_shutdown, 0x2F)
tof_timing = tof1.get_timing()

inductive_sensor = materialSensor.material_sensor(27, inductive=True)
capacitive_sensor = materialSensor.material_sensor(22, inductive=False)
    
def laser(x):
    if (x==1):
        GPIO.output(laserPin,GPIO.HIGH)
    else:
        GPIO.output(laserPin,GPIO.LOW)
        print("off")

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
    #file.write(str(dist1) + ", " + str(dist2) + ", " + str(dist3) + ", ")


def read_materials():
    metal_reading = inductive_sensor.detect_material()
    print("Inductive Sensor Reads: {}".format(metal_reading))
    capacitive_reading = capacitive_sensor.detect_material()
    print("Capacitive Sensor Reads: {}".format(capacitive_reading))
    
def objectFound():
    redLED()
    laser(0) 
    print("There an object")
    print("The size is:")
    size()
    #file.write(str(rc_time(pressurePad)) + "\n")
    read_materials()
    camera.take_picture()
    laser(1)
    greenLED()

def objectGone():
    print ("The object is gone")


def pressure():
    time.sleep(0.2)
    objectFound()
    objectGone()
    file.close()




while True:
    pressure()