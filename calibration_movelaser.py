#!/usr/bin/python3

# This will move servos on channels 1 and 3
# Tilt Servo (top) -- Channel 3:
#  Range: 200 (up) - 480 (down)
#
# Pan Servo (bottom) -- Channel 1:
#  Range: 160 (right) - 600 (left)


from __future__ import division
import time
import random

import sys
if sys.version_info[0] < 3: print("*********************************\n** Warning: Use python3 to run **\n*********************************")

# Set up GPIO for laser power control
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
laserPin = 23 # Broadcom pin 23 (P1 pin 16)
GPIO.setup(laserPin, GPIO.OUT)
GPIO.output(laserPin, GPIO.LOW)  # Initialize LOW

# Import the PCA9685 module.
import Adafruit_PCA9685

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Servo addresses
pan = 3
tilt = 1

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
# Pulse length out of 4096
pan_min = 160+200   # Default = 160
pan_mid = 380	# Default = 380
pan_max = 600   # Default = 600
tilt_min = 200  # Default = 200
tilt_mid = 340	# Default = 340
tilt_max = 480  # Default = 480

pan_cur = pan_mid
tilt_cur = tilt_mid

pwm_freq = 50   # Default = 60

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(pwm_freq)

def setPan(t):
	pwm.set_pwm(pan, 0, t)
	global pan_cur
	pan_cur = t

def setTilt(t):
	pwm.set_pwm(tilt, 0, t)
	global tilt_cur
	tilt_cur = t

GPIO.output(laserPin, GPIO.HIGH)  # Turn laser on

axis = input("Move what?  [P]an [T]ilt  ")

### Pan ###
if axis.lower() == "p":
	newTilt = input("Choose tilt (200-480): ")
	setTilt(int(newTilt))
	while True:
		mode = input("Mode?  [R]ange [S]et  ")
		if mode.lower() == "r":
			# Cycle through a range of pan values 3 times
			while True:
				rng = [160, 600]
				rng[0] = int(input("Range - Lower bound (160-600): "))
				rng[1] = int(input("Range - Upper bound (160-600): "))
				for _ in range(3):
					# Move servo by 10 at a time until upper bound is reached, then go back to lower bound
					for i in range(rng[0], rng[1], 10):
						setPan(int(i))
						time.sleep(0.1)
					for i in range(rng[1], rng[0], -10):
						setPan(int(i))
						time.sleep(0.1)


		else:
			# Pick a single pan value to move to
			while True:
				newPan = input("Set pan (160-600): ")
				setPan(int(newPan))

### Tilt ###
else:
	newPan = input("Choose pan (160-600): ")
	setPan(int(newPan))
	while True:
		mode = input("Mode?  [R]ange [S]et  ")
		if mode.lower() == "r":
			# Cycle through a range of tilt values 3 times
			while True:
				rng = [200, 480]
				rng[0] = int(input("Range - Lower bound (200-480): "))
				rng[1] = int(input("Range - Upper bound (200-480): "))
				for _ in range(3):
					# Move servo by 10 at a time until upper bound is reached, then go back to lower bound
					for i in range(rng[0], rng[1], 10):
						setTilt(int(i))
						time.sleep(0.1)
					for i in range(rng[1], rng[0], -10):
						setTilt(int(i))
						time.sleep(0.1)


		else:
			# Pick a single tilt value to move to
			while True:
				newTilt = input("Set tilt (200-480): ")
				setTilt(int(newTilt))
