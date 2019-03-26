import numpy as np
import cv2 as cv
from picamera import PiCamera
import math
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

camera = PiCamera()

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

def center_of_detected(x,y,w,h):
    #returns the center of the detected area
    x = x + (w/2)
    y = y + (h/2)
    return int(x),int(y)

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
    else:
        print('RotationCW: ' + str(rot))
        rotateCW(int(rot))
        return rot


face_cascade  = cv.CascadeClassifier('haarcascade_frontalface_defualt.xml')

while 1:
    camera.capture('tex.jpg')
    img = cv.imread('tex.jpg')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    d,h = center_of_image(img)
    cv.circle(img,(d,h), 4, (0,0,255), -1)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        x,y = center_of_detected(x,y,w,h)
        x = distance_from_center(d, x)
        degree = rotation_for_camera(d, x)
        print('D: ' + str(degree))
        print('x: ' + str(x))
        print('y: ' + str(y))
