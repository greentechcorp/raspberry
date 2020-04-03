#!/usr/bin/python

# MIT License
# 
# Copyright (c) 2017 John Bryan Moore
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import VL53L0X
import RPi.GPIO as GPIO

# GPIO for Sensor 1 shutdown pin
sensor1_shutdown = 17
# GPIO for Sensor 2 shutdown pin
sensor2_shutdown = 27
# GPIO for Sensor 3 shutdown pin
sensor3_shutdown = 22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class tof_sensor:
	def __init__(self, shutdown_pin, i2c_address):
		self.shutdown_pin = shutdown_pin
		GPIO.setup(shutdown_pin, GPIO.OUT)
		GPIO.output(shutdown_pin, GPIO.LOW)
		time.sleep(0.50)
		
		self.tof = VL53L0X.VL53L0X(address=i2c_address)
		
		GPIO.output(shutdown_pin, GPIO.HIGH)
		time.sleep(0.50)
		self.tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
		
	def get_timing(self):
		timing = self.tof.get_timing()
		if (timing < 20000):
			timing = 20000
		return timing
		
	def get_distance(self, timing=None):
		if not timing:
			timing = self.get_timing
		return self.tof.get_distance()
		
	def cleanup(self):
		self.tof.stop_ranging()
		GPIO.output(self.shutdown_pin, GPIO.LOW)
		
	def __del__(self):
		self.cleanup()

