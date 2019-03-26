import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from opencv_detect import calculateXDistance
import sys
#pin setup
increment = 6

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
        distance, image_width = calculateXDistance(image)
        print('picture taken')
        return distance, image_width
    else:
        return None, None

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

def activetrackbusstop():
    x = 1
    while x==1:
        picthentrack(increment)
        increment++
        
    print('Bus stop locked on: Engaging Autopilot.')

def picthentrack(num):
    distance, image_width = TakePicture(num)
    if distance:
        rotation_for_camera(image_width, distance)

def StepperMovement():
    #stepper predetermined motions
    picthentrack(0)
    rotateCW(60)

    picthentrack(1)
    #time.sleep(.5)
    rotateCW(60)

    picthentrack(2)
    #time.sleep(.5)
    rotateCCW(180)

    picthentrack(3)
    #time.sleep(.5)
    rotateCCW(60)

    picthentrack(4)
    #time.sleep(.5)
    rotateCW(120)

def TransmitImage():
    #send an image over bluetooth
    print('Transmiting image to ... phone')

def center_of_image(img):
    width, height = img.shape[:2]
    print(width)
    print(height)
    x = width/2
    y = height/2
    return int(x),int(y)

def distance_from_center(center_x, face_x):
    distance = center_x - face_x
    print('Distance: ' + str(distance))
    return distance

def rotation_for_camera(image_width, dfc):
    ppd = image_width/62
    d = dfc/ppd
    rot = math.floor(d/ 1.8)
    if dfc < 0:
        print('RotationCCW: ' + str(rot))
        rotateCCW(int(-1 * rot))
        return rot
    elif dfc > 0:
        print('RotationCW: ' + str(rot))
        rotateCW(int(rot))
        return rot
    else:
        print('********Centered**********')

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
