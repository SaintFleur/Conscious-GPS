import RPi.GPIO as GPIO
import wiringpi
import time

wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

delay_period = .01
x = 1
while x==1:
    for pulse in range(50, 250, 1):
        wiringpi.pwmWrite(18, pulse)
        time.sleep(delay_period)
    for pulse in range(250, 50, -1):
        wiringpi.pwmWrite(18, pulse)
        time.sleep(delay_period)
    x = 0

wiringpi.pinMode(18, wiringpi.GPIO.INPUT)    
