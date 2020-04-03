import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER_1 = 18
GPIO_ECHO_1 = 23

GPIO_TRIGGER_2 = 17
GPIO_ECHO_2 = 22
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER_1, GPIO.OUT)
GPIO.setup(GPIO_ECHO_1, GPIO.IN)
GPIO.output(GPIO_TRIGGER_1, False)

GPIO.setup(GPIO_TRIGGER_2, GPIO.OUT)
GPIO.setup(GPIO_ECHO_2, GPIO.IN)
GPIO.output(GPIO_TRIGGER_2, False)
 
def distance(trigger,echo):
    print("Sent trigger for distance measurement")
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(echo) == 0:
        StartTime = time.time()

    while GPIO.input(echo) == 1:
        StopTime = time.time()
    print("Received distance measurement")
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
 
 
if __name__ == '__main__':
    try:
        print("Sensors settling...")
        time.sleep(2) 
        while True:
            dist2 = distance(GPIO_TRIGGER_1,GPIO_ECHO_1)
            dist1 = distance(GPIO_TRIGGER_2,GPIO_ECHO_2)
            print ("Measured Distance = %.1f cm, %.1f cm" % (dist1, dist2))
            time.sleep(0.2)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
