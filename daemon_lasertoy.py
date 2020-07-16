#!/usr/bin/python3

## This program will run in the background and start the lasertoy.py routine at a certain time

import time
import datetime as dt
import lasertoy

log_daemonlog = r"/home/pi/Scripts/lasertoy/daemon.log"

# Main loop
while True:

	# Get current time
	curtime = dt.datetime.now(dt.timezone(-dt.timedelta(hours=4))).time()

	# Run for 45 minutes at 12pm, then 30 minutes at 5pm
	if (curtime.hour == 12+1 and curtime.minute <= 1):
		with open(log_daemonlog, 'a') as f: f.write('{} {}: Running laser routine at 12pm (12:00) for 45 minutes.\n'.format(time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S")))

		lasertoy.runLaserRoutine(timer_mins=45)

		with open(log_daemonlog, 'a') as f: f.write('{} {}: Finished running laser routine from 12pm (12:00).\n'.format(time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S")))


	elif (curtime.hour == 12+6 and curtime.minute <= 1):
		with open(log_daemonlog, 'a') as f: f.write('{} {}: Running laser routine at 5pm (17:00) for 30 minutes.\n'.format(time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S")))

		lasertoy.runLaserRoutine(timer_mins=30)

		with open(log_daemonlog, 'a') as f: f.write('{} {}: Finished running laser routine from 5pm (17:00).\n'.format(time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S")))




	# Sleep until the top of the next hour
	curdt = dt.datetime.now(dt.timezone(-dt.timedelta(hours=4)))

	nexthour = curdt.replace(hour=curdt.hour, minute=0, second=0, microsecond=0) + dt.timedelta(hours=1, seconds=2)

	tts = (nexthour - curdt).seconds

	with open(log_daemonlog, 'a') as f: f.write('{} {}: Sleeping for {} seconds (about {} minutes) to the next hour.\n'.format(time.strftime("%m/%d/%Y"), time.strftime("%H:%M:%S"), tts, int(tts/60)))

	time.sleep(tts)
