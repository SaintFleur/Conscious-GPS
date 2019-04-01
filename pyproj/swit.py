import RPi.GPIO as GPIO
import time

swi = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(swi, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while 1:
        if GPIO.input(swi):
            #this tells the raspi that the switched has been pressed can be used in the homing code

            print('pressed')
        else:
            #the button has not been pressed here
            print('not ready')

except KeyboardInterrupt:
    print('Josiah you fool')
    GPIO.cleanup()
