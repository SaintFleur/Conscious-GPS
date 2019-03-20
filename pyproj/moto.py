import RPi.GPIO as GPIO
import time

stp = 2
dir = 3
MS1 = 4
MS2 = 17
ene = 27
butt = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(stp, GPIO.OUT)
GPIO.setup(dir, GPIO.OUT)
GPIO.setup(MS1, GPIO.OUT)
GPIO.setup(MS2, GPIO.OUT)
GPIO.setup(ene, GPIO.OUT)
GPIO.setup(butt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(stp, GPIO.LOW)
GPIO.output(dir, GPIO.LOW)

def StepForwardDefualt():
    print('Moving forward at defualt step mode')
    GPIO.output(dir, GPIO.LOW)

    for x in range(30):
        GPIO.output(stp, GPIO.HIGH)
        time.sleep(.0001)
        GPIO.output(stp, GPIO.LOW)
        time.sleep(.0001)

def StepReverseDefualt():
    print('Moving in reverse at defualt step mode')
    GPIO.output(dir, GPIO.HIGH)

    for x in range(30):
        GPIO.output(stp, GPIO.HIGH)
        time.sleep(.001)
        GPIO.output(stp, GPIO.LOW)
        time.sleep(.001)

print('welcome')

try:
    while 1:
        if GPIO.input(butt):
            xvd = 10
        else:
            StepReverseDefualt()
            time.sleep(1)
            print('ready')
except KeyBoardInterrupt:
    GPIO.cleanup()
