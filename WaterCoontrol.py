
import pygame
import RPi.GPIO as GPIO
import time

# Set up pins
MotorPin1   = 17
MotorPin2   = 27
MotorEnable = 22
TRIG = 23
ECHO = 24
NOMICIR=0
directions = {'CW': 1, 'CCW': -1, 'STOP': 0}





def setup():
	# Set the GPIO modes to BCM Numbering
	GPIO.setmode(GPIO.BCM)
	# Set pins to output
	GPIO.setup(MotorPin1, GPIO.OUT)
	GPIO.setup(MotorPin2, GPIO.OUT)
	GPIO.setup(MotorEnable, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)



# Define a motor function to spin the motor
# direction should be 
# 1(clockwise), 0(stop), -1(counterclockwise)
def motor(direction):
	# Clockwise
	if direction == 1:
		# Set direction
		GPIO.output(MotorPin1, GPIO.HIGH)
		GPIO.output(MotorPin2, GPIO.LOW)
		# Enable the motor
		GPIO.output(MotorEnable, GPIO.HIGH)
		print ("Clockwise")
	# Counterclockwise
	if direction == -1:
		# Set direction
		GPIO.output(MotorPin1, GPIO.LOW)
		GPIO.output(MotorPin2, GPIO.HIGH)
		# Enable the motor
		GPIO.output(MotorEnable, GPIO.HIGH)
		print ("Counterclockwise")
	# Stop
	if direction == 0:
		# Disable the motor
		GPIO.output(MotorEnable, GPIO.LOW)
		print ("Stop")

def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.000002)

	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

	
	while GPIO.input(ECHO) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100

def checkCall():
    print("call start")
    pygame.mixer.init()
    pygame.mixer.music.load("sakekas.mp3")
    pygame.mixer.music.play(1)
    time.sleep(2)
    pygame.mixer.music.stop()
    time.sleep(10.0)

def loop():
    print("pass")
    count=0
		#time.sleep(5)
    while True:
        dis = distance()
        if 10<dis and dis<1000:
            count+=1
        else:
            count=0
        if count>3:
            checkCall()
            count=0
        print ('Distance: %.2f' % dis)
        time.sleep(0.3)

def pour_sake():
	motor(directions['CW'])
	time.sleep(10)
	motor(directions['STOP'])

def main():
	count=0

	# Define a dictionary to make the script more readable
	# CW as clockwise, CCW as counterclockwise, STOP as stop
	# directions = {'CW': 1, 'CCW': -1, 'STOP': 0}
	pouring_is_needed = True
	while True:
		
		# Clockwise
		#time.sleep(5)
		#time.sleep(5)
		# Stop
		#if 10<dis and dis<1000:
		motor(directions['STOP'])
		#time.sleep(5)
	

		dis = distance()
		if 10<dis and dis<1000:#A cup does not exist
			count+=1
		else:# A cup exists
			count=0
			if pouring_is_needed==True:
				pour_sake()
				pouring_is_needed=False
		if count>3:
			checkCall()
			pouring_is_needed=True
			count=0
		print ('Distance: %.2f' % dis)
		time.sleep(0.3)


def destroy():
	# Stop the motor
	GPIO.output(MotorEnable, GPIO.LOW)
	# Release resource
	GPIO.cleanup()    

# If run this script directly, do:
if __name__ == '__main__':
	setup()
	try:
		main()
	# When 'Ctrl+C' is pressed, the program 
	# destroy() will be executed.
	except KeyboardInterrupt:
		destroy()