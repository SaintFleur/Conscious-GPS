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
homing = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(stp, GPIO.OUT)
GPIO.setup(dir, GPIO.OUT)
GPIO.setup(MS1, GPIO.OUT)
GPIO.setup(MS2, GPIO.OUT)
GPIO.setup(ene, GPIO.OUT)
GPIO.setup(butt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(homing, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(stp, GPIO.LOW)
GPIO.output(dir, GPIO.LOW)

curve_speed = 15
#camera setup

camera = PiCamera()

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
    image = camera.capture(string1 + str(integer) + string2)
    if(image):
        distance, image_width = calculateXDistance(image)
        print('picture taken')
        return distance, image_width
    else:
        return None, None

def rotateCW(z):
    #rotate clockwise
    print('rotating clockwise')
    GPIO.output(dir, GPIO.HIGH)
    inc = ( z/curve_speed) * .001
    counter = 0
    for x in range(z):
        GPIO.output(stp, GPIO.HIGH)
        time.sleep(inc)
        GPIO.output(stp, GPIO.LOW)
        time.sleep(inc)
        counter += 1
        if counter < (x/2):
            inc = inc - .001
        else:
            inc = inc +.001

def step(y):
    #step function to be called upon
    GPIO.output(stp, GPIO.HIGH)
    time.sleep(y)
    GPIO.output(stp, GPIO.LOW)
    time.sleep(y)

#Trying to change the code to reduce the speed of the motor in the beginning and at the end
def rotate_CW(z):
    # rotatates clockwise I think
    print('rotating clockwise')
    GPIO.output(dir, GPIO.HIGH)
    for x in range(z):
        if x < (z*.1) or x > (z - (z*.1)):
            step(.002)
        else:
            step(.001)

def rotate_CCW(z):
    #rotates counter clock wise probably
    print("rotating counter clockwise")
    GPIO.output(dir, GPIO.LOW)
    for x in range(z):
        if x < (z*.1) or x > (z - (z*.1)):
            step(.005)
        else:
            step(.001)

def rotateCCW(z):
    #rotate counter clockwise
    print('rotating counter clockwise')
    GPIO.output(dir, GPIO.LOW)
    inc = ( z/curve_speed) * .001
    counter = 0
    for x in range(z):
        GPIO.output(stp, GPIO.HIGH)
        time.sleep(inc)
        GPIO.output(stp, GPIO.LOW)
        time.sleep(inc)
        counter += 1
        if counter < (x/2):
            inc = inc - .001
        else:
            inc = inc +.001

def home():
    #Homing function to allow the raspberry pi to home itself
    #Should be called after the bus stop is lost or at the start of the file
    check = 1;
    while check:
        if GPIO.input(homing):
            #this tells the raspi that the switched has been pressed can be used in the homing code
            print('The incredible journey has ended')
            check = 0
        else:
            #the button has not been pressed here
            StepReverseDefualt(1)
            print('Homeward Bound')

def activetrackbusstop():
    x = 1
    while x==1:
        picthentrack(increment)
        increment+=1

    print('Bus stop locked on: Engaging Autopilot.')

def picthentrack(num):
    distance, image_width = TakePicture(num)
    if distance:
        rotation_for_camera(image_width, distance)

def StepperMovement():
    #stepper predetermined motions
    picthentrack(0)
    rotate_CW(33)

    picthentrack(1)
    #time.sleep(.5)
    rotate_CW(33)

    picthentrack(2)
    #time.sleep(.5)
    rotate_CCW(99)

    picthentrack(3)
    #time.sleep(.5)
    rotate_CCW(33)

    picthentrack(4)
    #time.sleep(.5)
    rotate_CW(66)

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
    print('welcome to the Incredible Journey')
    home()
    while 1:
        if GPIO.input(butt):
            xvd = 10
        else:
            StepperMovement()
            time.sleep(1)
            print('ready')
except KeyboardInterrupt:
    print('Josiah is a fool')
    GPIO.cleanup()


#Why do I have to this
#probably because of Josiah
#Trying to change the code to reduce the speed of the motor in the beginning and at the end
