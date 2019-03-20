from picamera import PiCamera
from time import sleep

camera = PiCamera()
for integer in range(5):
    string1 = "imagine"
    string2 = ".jpg"
    camera.capture(string1 + str(integer) + string2)
