import time
import RPi.GPIO as GPIO

class material_sensor:
  def __init__(self, pin, inductive=True):
    self.GPIOpin = pin
    self.inductive = inductive
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.GPIOpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    if inductive:
      print("Initialized Inductive Sensor at pin {}".format(pin))
    else:
      print("Initialized Capacitive Sensor at pin {}".format(pin))
    
    
  def take_reading(self):
    state = GPIO.input(self.GPIOpin)
    if state:
      if self.inductive:
        return False
      else:
        return True
    else:
      if self.inductive:
        return True
      else:
        return False
      
  def detect_material(self, readings=5, threshold=1):
    counter = 0
    for _ in range(readings):
      detected_material = self.take_reading()
      time.sleep(0.2)
      if detected_material:
        counter += 1
        if counter >= threshold:
          return True
    return False
