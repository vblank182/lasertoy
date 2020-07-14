# This will move servos on channels 1 and 3
# Tilt Servo (top) -- Channel 3:
#  Range: 200 (down) - 480 (up)
#
# Pan Servo (bottom) -- Channel 1:
#  Range: 160 (right) - 600 (left)


from __future__ import division
import time
import random

pan_reset = 320		# 
tilt_reset = 350	# Up = -, Down = +

# Set up GPIO for laser power control
import RPi.GPIO as GPIO

# Import the PCA9685 module.
import Adafruit_PCA9685

# Servo addresses
pan = 1
tilt = 3

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

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

def resetServos():
	setPan(pan_reset)
	setTilt(tilt_reset)

if __name__ == "__main__":
	# Make sure laser is off
	GPIO.setmode(GPIO.BCM)
	laserPin = 23 # Broadcom pin 23 (P1 pin 16)
	GPIO.setup(laserPin, GPIO.OUT)
	GPIO.output(laserPin, GPIO.LOW)  # Initialize LO
	GPIO.cleanup()

	# Reset servos to default position
	print('Resetting servos to rest position.')
	resetServos()
