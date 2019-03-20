import RPi.GPIO as GPIO
import time

led = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

while 1:
    GPIO.output(led, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(led, GPIO.LOW)
    time.sleep(2)

GPIO.cleanup()
