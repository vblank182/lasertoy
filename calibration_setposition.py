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
import resetservos

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
pan = 1
tilt = 3

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

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

def setPan(t):
	pwm.set_pwm(pan, 0, t)
	global pan_cur
	pan_cur = t
	
def setTilt(t):
	pwm.set_pwm(tilt, 0, t)
	global tilt_cur
	tilt_cur = t
	
GPIO.output(laserPin, GPIO.HIGH)  # Turn laser on

while True:
	print("-- Set servo position (enter q to quit): --")
	p = input("Set pan (160-600): ")
	t = input("Set tilt (200-480): ")
	if (p.lower() == "q" or t.lower() == "q"):
		break
	setPan(int(p))
	setTilt(int(t))

print("Quitting...")
GPIO.output(laserPin, GPIO.LOW)  # Turn laser off
GPIO.cleanup()
resetservos.resetServos()
