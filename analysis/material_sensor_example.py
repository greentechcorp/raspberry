import time
import RPi.GPIO as GPIO
import materialSensor

inductive_sensor = materialSensor.material_sensor(23, inductive=True)
capacitive_sensor = materialSensor.material_sensor(24, inductive=False)

def read_capacitive():
    capacitive_reading = capacitive_sensor.detect_material(readings=1, threshold=1)
    print("Capacitive Sensor Reads: {}\n".format(capacitive_reading))

def read_inductive():
    metal_reading = inductive_sensor.detect_material()
    print("Inductive Sensor Reads: {}\n".format(metal_reading))
 
def read_materials():
    read_capacitive()
    read_inductive()

while True:
    #read_inductive()
    read_capacitive()
