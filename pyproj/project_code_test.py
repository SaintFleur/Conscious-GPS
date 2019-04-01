import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from picamera import array
from opencv_detect import calculateXDistance
#pin setup

stp = 2
dir = 3
MS1 = 4
MS2 = 17
ene = 27
butt = 22
homing = 26


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

def home():
    #Homing function to allow the raspberry pi to home itself
    #Should be called after the bus stop is lost or at the start of the file
    check = 1;
    while check:
        if GPIO.input(swi):
            #this tells the raspi that the switched has been pressed can be used in the homing code
            print('The incredible journey has ended')
            check = 0
        else:
            #the button has not been pressed here
            StepReverseDefualt(1)
            print('Homeward Bound')


    print('Follow the North star')

def StepForwardDefualt(y):
    print('Moving forward at defualt step mode')
    GPIO.output(dir, GPIO.LOW)

    for x in range(y):
        GPIO.output(stp, GPIO.HIGH)
        time.sleep(.001)
        GPIO.output(stp, GPIO.LOW)
        time.sleep(.001)

def StepReverseDefualt(y):
    print('Moving in reverse at defualt step mode')
    GPIO.output(dir, GPIO.HIGH)

    for x in range(y):
        GPIO.output(stp, GPIO.HIGH)
        time.sleep(.001)
        GPIO.output(stp, GPIO.LOW)
        time.sleep(.001)


def  TakePicture(integer):
    string1 = "imagine"
    string2 = ".jpg"
    # image = camera.capture(string1 + str(integer) + string2)
    image = None

    with camera as cam:
        cam.start_preview()
        time.sleep(2)
        with array.PiRGBArray(cam) as stream:
            cam.capture(stream, format='bgr')
            # At this point the image is available as stream.array
            image = stream.array
        cam.capture(string1 + str(integer) + string2)
    print('picture taken')
    if(image == None):
        return None
    else:
        distance = calculateXDistance(image)
        return distance
    # else:
    #     return None




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


try:
    print('Welcome to the Matrix ')
    home()
    while 1:
        if GPIO.input(butt):
            xvd = 10
        else:
            StepperMovement()
            time.sleep(1)
            print('ready')
except KeyboardInterrupt:
    print('Josiah you fool')
    GPIO.cleanup()
