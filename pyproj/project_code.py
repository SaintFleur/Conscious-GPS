import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from opencv_detect import calculateXDistance
#pin setup

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

#camera setup

camera = PiCamera()

def StepForwardDefualt():
    print('Moving forward at defualt step mode')
    GPIO.output(dir, GPIO.LOW)

    for x in range(30):
        GPIO.output(stp, GPIO.HIGH)
        time.sleep(.001)
        GPIO.output(stp, GPIO.LOW)
        time.sleep(.001)

def StepReverseDefualt():
    print('Moving in reverse at defualt step mode')
    GPIO.output(dir, GPIO.HIGH)

    for x in range(30):
        GPIO.output(stp, GPIO.HIGH)
        time.sleep(.001)
        GPIO.output(stp, GPIO.LOW)
        time.sleep(.001)


def  TakePicture(integer):
    string1 = "imagine"
    string2 = ".jpg"
    image = camera.capture(string1 + str(integer) + string2)
    if(image):
        distance = calculateXDistance(image)
        print('picture taken')
        return distance
    else:
        return None




def rotateCW(x):
    #rotate clockwise
    print('rotating clockwise')
    GPIO.output(dir, GPIO.HIGH)

    for x in range(x):
        GPIO.output(stp, GPIO.HIGH)
        time.sleep(.001)
        GPIO.output(stp, GPIO.LOW)
        time.sleep(.001)

def rotateCCW(x):
    #rotate counter clockwise
    print('rotating counter clockwise')
    GPIO.output(dir, GPIO.LOW)

    for x in range(x):
        GPIO.output(stp, GPIO.HIGH)
        time.sleep(.001)
        GPIO.output(stp, GPIO.LOW)
        time.sleep(.001)

def StepperMovement():
    #stepper predetermined motions
    print(TakePicture(0))
    rotateCW(60)

    print(TakePicture(1))
    #time.sleep(.5)

    rotateCW(60)

    print(TakePicture(2))
    #time.sleep(.5)

    rotateCCW(180)

    print(TakePicture(3))

    #time.sleep(.5)

    rotateCCW(60)

    print(TakePicture(4))

    #time.sleep(.5)

    rotateCW(120)


def TransmitImage():
    #send an image over bluetooth
    print('Transmiting image to ... phone')

def trackstop(inny):
    if inny > 0:
        rotateCW(inny)
    elif inny < 0:
        rotateCCW(-1*inny)
    else:
        print("centered")


def pixtodeg(pix):
    distance = calculateXDistance
    deg  = pix
    return deg


print('welcome')

try:
    while 1:
        if GPIO.input(butt):
            xvd = 10
        else:
            StepperMovement()
            time.sleep(1)
            print('ready')
except KeyBoardInterrupt as ky:
    print(ky)
    GPIO.cleanup()
