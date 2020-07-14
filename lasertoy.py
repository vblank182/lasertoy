#!/usr/bin/python3

# This will move servos on channels 1 and 3
# Tilt Servo (top) -- Channel 3:
#  Range: 200 (up) - 350 (down)
#
# Pan Servo (bottom) -- Channel 1:
#  Range: 350 (right) - 500 (left)


from __future__ import division
import time
import random
import resetservos

log_runlog = r"/home/pi/Scripts/LaserToy/run.log"
log_diag = r"/home/pi/Scripts/LaserToy/diagnostic.log"

# Set up GPIO for laser power control
import RPi.GPIO as GPIO

## Import the PCA9685 module.
# Reference: https://learn.adafruit.com/16-channel-pwm-servo-driver/library-reference
# Source: https://github.com/adafruit/Adafruit_Python_PCA9685/blob/master/Adafruit_PCA9685/PCA9685.py
import Adafruit_PCA9685

# Servo addresses
pan = 1
tilt = 3

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
# Pulse length out of 4096
pan_min = 260   # Default = 260
pan_mid = 340    # Default = 340
pan_max = 450   # Default = 450
tilt_min = 200  # Default = 200
tilt_mid = 280    # Default = 280
tilt_max = 325  # Default = 325

pan_reset = 320        #
tilt_reset = 350    # Up = -, Down = +

pwm_freq = 50   # Default = 60

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000      # 1,000,000 us per second
    pulse_length //= pwm_freq   # Frequency in Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096       # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

def setPan(t):
    pwm.set_pwm(pan, 0, t)
    global pan_cur
    pan_cur = t

def setTilt(t):
    pwm.set_pwm(tilt, 0, t)
    global tilt_cur
    tilt_cur = t

def full_on():
    # Sets both servo pins full on (100% duty cycle)
    pwm.setPWM(pan, 4096, 0);
    pwm.setPWM(tilt, 4096, 0);

def full_off():
    # Sets both servo pins full off (0% duty cycle)
    pwm.setPWM(pan, 0, 4096);
    pwm.setPWM(tilt, 0, 4096);


def panTo(target):
    ## WIP: Speed controlled pan
    steps = 20

    for tick in range (0, steps):
        inc = (target - pan_cur) / steps        # find increment size
        setPan( int(pan_cur + inc*(tick+1)) )    # take steps toward target

        time.sleep(0.01)

#### Movement algorithm ####
# Move in tiny steps on a very short delay, but randomly decide to move in larger, quicker steps with a longer delay.
# Occasionally, when on the wall, stop for an extended period of time.
#
############################

def mediumSteps():
    pan_step = 25
    tilt_step = 15

    nextpan = random.randint(pan_cur-pan_step, pan_cur+(pan_step+1))

    if (nextpan <= pan_min):
        nextpan = nextpan + 2*pan_step
    if (nextpan >= pan_max):
        nextpan = nextpan - 2*pan_step

    setPan(nextpan)


    nexttilt = random.randint(tilt_cur-tilt_step, tilt_cur+(tilt_step+1))

    if (nexttilt <= tilt_min):
        nexttilt = nexttilt + 2*tilt_step
    if (nexttilt >= tilt_max):
        nexttilt = nexttilt - 2*tilt_step

    setTilt(nexttilt)

    time.sleep(random.randint(10, 26)/100)  # Sleep for a random time from 0.1 seconds to 0.25 seconds.

def shortSteps():
    pan_step = 5
    tilt_step = 5

    nextpan = random.randint(pan_cur-pan_step, pan_cur+(pan_step+1))

    if (nextpan <= pan_min):
        nextpan = nextpan + 2*pan_step
    if (nextpan >= pan_max):
        nextpan = nextpan - 2*pan_step

    setPan(nextpan)


    nexttilt = random.randint(tilt_cur-tilt_step, tilt_cur+(tilt_step+1))

    if (nexttilt <= tilt_min):
        nexttilt = nexttilt + 2*tilt_step
    if (nexttilt >= tilt_max):
        nexttilt = nexttilt - 2*tilt_step

    setTilt(nexttilt)

    time.sleep(random.randint(5, 16)/100)  # Sleep for a random time from 0.05 seconds to 0.015 second.

def wait():
    chance = random.randint(0, 100)
    if (random.randint(0, 100) < 10):
        # There is a 10% chance we will wait for a short period.
        time.sleep(2)
    elif (random.randint(0, 100) < 4):
        # There is a 4% chance we will wait for a long period.
        time.sleep(4)
    elif (random.randint(0, 100) < 1):
        # There is a 1% chance we will wait for a longer period.
        time.sleep(9)

def resetServos():
    setPan(pan_reset)
    setTilt(tilt_reset)



def runLaserRoutine(timer_mins=45, daemon=True):

    # Log file
    if daemon: msg = "from daemon"
    else: msg = "manually"

    with open(log_runlog, 'a') as f:
        f.write('Run {} on {} at {}.\n'.format(msg, time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S")))


    with open(log_diag, 'a') as f:
        f.write('{} {}: Starting laser routine.\n'.format(time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S")))

        # Initialize laser GPIO
        GPIO.setmode(GPIO.BCM)
        laserPin = 23  # Broadcom pin 23 (P1 pin 16)
        GPIO.setup(laserPin, GPIO.OUT)
        GPIO.output(laserPin, GPIO.LOW)  # Initialize LOW (off)
        f.write('{} {}: Initialized GPIO.\n'.format(time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S")))

        # Set servo PWM frequency
        pwm.set_pwm_freq(pwm_freq)

        setPan(pan_mid)
        f.write('{} {}: Set initial pan.\n'.format(time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S")))

        setTilt(tilt_mid)
        f.write('{} {}: Set initial tilt.\n'.format(time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S")))

        # Set servo variables to match initial servo positions
        pan_cur = pan_mid
        tilt_cur = tilt_mid

        # Get time that program started for timer purposes.
        starttime = time.time()
        # Set a time at which program will end.
        endtime = starttime + (timer_mins)*60


        GPIO.output(laserPin, GPIO.HIGH)  # Turn laser on
        f.write('{} {}: Laser GPIO switched on.\n'.format(time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S")))


        # Run until timer has elapsed
        lastWait = 0
        while (time.time() < endtime):
            chance = random.randint(0, 100)

            # Take either short or medium steps on a chance
            if (chance < 60):
                shortSteps()
            else:
                mediumSteps()

            # When laser is within top half of tilt range, roll to wait
            waitCooldown = 5  # seconds to wait before we can wait again
            if (220 <= tilt_cur <= 290 and (time.time()-lastWait) > waitCooldown):
                wait()
                lastWait = time.time()  # record the last wait so we don't wait too often


        f.write('{} {}: Routine finished. Disabling laser and resetting servos.\n'.format(time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S")))
        GPIO.output(laserPin, GPIO.LOW)  # Turn laser off
        f.write('{} {}: Laser GPIO switched off.\n'.format(time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S")))

        # Make sure laser is off
        GPIO.setmode(GPIO.BCM)
        laserPin = 23 # Broadcom pin 23 (P1 pin 16)
        GPIO.setup(laserPin, GPIO.OUT)
        GPIO.output(laserPin, GPIO.LOW)  # Initialize LO

        resetServos()
        full_off()

        GPIO.cleanup()

        f.write('{} {}: Servos reset. Finished lasertoy.py script.\n'.format(time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S")))
    ## End of laser routine


if __name__ == "__main__":
    print('Moving servos, press Ctrl-C to quit...')
    runLaserRoutine(daemon=False)
