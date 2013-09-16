import socket
import os
from Adafruit_PWM_Servo_Driver import PWM


# This is what gets your IP as a string (from Stackoverflow):
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("192.168.0.254", 80))
UDP_IP = s.getsockname()[0]
s.close
UDP_PORT = 4444
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print "Listening to IP " + UDP_IP + ":" + str(UDP_PORT)	


# Servo setup:
pwm = PWM(0x40, debug=True)
servoMin = 122  # Min pulse length out of 4096
servoMax = 492  # Max pulse length out of 4096
pwm.setPWMFreq(50) 
xServo = 0;
yServo = 1;

servoNeutral = ((servoMax - servoMin) / 2) + servoMin

#position setup:
xRange = 150
yRange = 150

def updatePosition(x, y):
	pwm.setPWM(xServo, 0, x)
	pwm.setPWM(yServo, 0, y)

def mapValues(inputX, inputMin, inputMax, outputMin, outputMax):
	return (inputX - inputMin) * (outputMax - outputMin) / (inputMax - inputMin) + outputMin

updatePosition(servoNeutral, servoNeutral)

print "waiting for first UDP message for neutral position..."
data, add = sock.recvfrom(1024)
xyz = data.split(",")
neutralX = float(xyz[0])
minX = neutralX - (xRange / 2.0)
maxX = neutralX + (xRange / 2.0)
neutralY = float(xyz[1])
minY = neutralY - (yRange / 2.0)
maxY = neutralY + (yRange / 2.0)

while True:
	data, add = sock.recvfrom(1024) # buffer = 1024 bytes
	xyz = data.split(",")
	os.system('clear')
	print "x:",  xyz[0] , " y: " , xyz[1] , " z: " , xyz[2]
	xFloat = float(xyz[0])
	yFloat = float(xyz[1])
	xPos = mapValues (xFloat, minX, maxX , servoMin, servoMax)
	yPos = mapValues (yFloat, minY, maxY , servoMin, servoMax)
	updatePosition(int(xPos), int(yPos))


