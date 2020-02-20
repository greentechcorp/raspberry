
import time
import VL53L0X
import RPi.GPIO as GPIO


tofSensors = [6,13,19,26]

inductivePin = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def initiateToF():
    for i in range (len(tofSensors)):
        GPIO.setup(tofSensors[i], GPIO.OUT)
        GPIO.output(tofSensors[i], GPIO.LOW)

    time.sleep(0.50)

    tof = [VL53L0X.VL53L0X(address=0x2B),VL53L0X.VL53L0X(address=0x2D),VL53L0X.VL53L0X(address=0x2E),VL53L0X.VL53L0X(address=0x2F)]

    for i in range (len(tofSensors)):
        GPIO.output(tofSensors[i], GPIO.HIGH)
        time.sleep(0.50)
        tof[i].start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    print("ToFs initialised")

def initiateInductive():
    GPIO.setup(inductivePin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    print("Intuctive initialised")
    print(inductivePin)

def detectMetal():
    state = GPIO.input(GPIOpin)
    if state:
      print("Metal")
    else:
      print("Not Metal")
    time.sleep(0.2)
  
def distances():
    for i in range(len(tofSensors)):
        distance = tof[i].get_distance()
        print ("sensor %d - %d mm" % (tof[i].my_object_number, distance))
    time.sleep(17/10)

def tofShutdown():
    for i in range(len(tofSensors)):
        tof[i].stop_ranging()
        GPIO.output(tofSensors[i], GPIO.LOW)

        