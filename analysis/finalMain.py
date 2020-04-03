import time
import csv
import camera
import VL53L0X
import RPi.GPIO as GPIO
import materialSensor
from hx711 import HX711

referenceUnit = -724.69
loadCellPinDT = 23
loadCellPinSCK = 24
tofSensors = [6,13,19,26]
inductivePin = 27
capPin = 5
ledPins = {"red": 22, "green": 17, "yellow": 27, "laser": 4}
boxLength = 220 #mm
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def initialise_leds():
    for _, led_pin in ledPins.items():
        GPIO.setup(led_pin, GPIO.OUT)
        GPIO.output(led_pin, GPIO.LOW)
   
def led(colour, on=True):
    gpioState = GPIO.HIGH if on else GPIO.LOW
    GPIO.output(ledPins[colour], gpioState)

def blink(colour):
    on = True
    for _ in range(10):
        led(colour, on=on)
        on = not on
        time.sleep(0.2)

def initialise_load_cell():
    load_cell = HX711(loadCellPinDT, loadCellPinSCK)
    load_cell.set_reading_format("MSB", "MSB")
    load_cell.set_reference_unit(referenceUnit)
    load_cell.reset()
    load_cell.tare()
    return load_cell

def initialise_tof():
    for i in range (len(tofSensors)):
        GPIO.setup(tofSensors[i], GPIO.OUT)
        GPIO.output(tofSensors[i], GPIO.LOW)

    time.sleep(0.50)

    tof = [VL53L0X.VL53L0X(address=0x2B),VL53L0X.VL53L0X(address=0x2D),VL53L0X.VL53L0X(address=0x2F),VL53L0X.VL53L0X(address=0x31)]

    for i in range (len(tofSensors)):
        GPIO.output(tofSensors[i], GPIO.HIGH)
        time.sleep(0.50)
        tof[i].start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    print("ToFs initialised")
    return tof

def initialise_inductive():
    GPIO.setup(inductivePin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    print("Inductive initialised")
    print(inductivePin)

def initialise_capacitive():
    GPIO.setup(capPin,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    print("Cap initialised")
    print(capPin)


def detect_metal():
    reading = input("Does the inductive sensor read metal? (y/n)")
    if reading == "y":
        return True
    if reading == "n":
        return False

def detect_cap():
    reading = input("Does the capacitive sensor register the object? (y/n)")
    if reading == "y":
        return True
    if reading == "n":
        return False

def get_distances(tofs):
    distances = []
    for i in range(len(tofSensors)):
        distance = tofs[i].get_distance()
        if distance > boxLength:
            distance = boxLength
        distances.append(distance)
        print ("sensor %d - %d mm" % (tofs[i].my_object_number, distance))
    time.sleep(1.5)
    return distances

def tof_shutdown():
    for i in range(len(tofSensors)):
        tof[i].stop_ranging()
        GPIO.output(tofSensors[i], GPIO.LOW)
    
def wait_for_object(load_cell):
    i = 0
    while int(load_cell.get_weight(5)) <= 0:
        print("Nothing detected by weight")
        time.sleep(0.2)
    time.sleep(0.2)
    
def read_sensor_data(load_cell, tof):
    time.sleep(1)
    weight = max(0, int(load_cell.get_weight(5)))
    distances = get_distances(tof)
    capacitive_reading = detect_cap()
    inductive_reading = detect_metal()
    return weight, distances[0], distances[1], distances[2], distances[3], capacitive_reading, inductive_reading
    
def write_sensor_data(label, sensor_data):
    with open('experiment_1_data.csv', 'a+', newline='') as csvfile:
        data_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        row_data = [label] + list(sensor_data)
        data_writer.writerow(row_data)
 
if __name__ == "__main__":
    tof = initialise_tof()
    load_cell = initialise_load_cell()
    inductiveSensor = materialSensor.material_sensor(inductivePin)
    initialise_capacitive()
    initialise_leds()
    while True:
        material_label = input("Enter the true label of the item being scanned (or 'exit'): ")
        if material_label == "exit":
            break
        
        #wait_for_object(load_cell)   #Commented out because weight sensor doesnt work
        sensor_data = read_sensor_data(load_cell, tof)
        write_sensor_data(material_label, sensor_data)
        camera.take_picture(material_label)
        blink("green")
        blink("laser")
        
    tof_shutdown()
