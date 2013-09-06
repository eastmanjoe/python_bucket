import Adafruit_BBIO.GPIO as GPIO
import time

GPIO.setup("P8_10", GPIO.OUT)
GPIO.setup("P8_12", GPIO.IN)

while True:
    if GPIO.input("P8_12"):
        GPIO.output("P8_10", GPIO.HIGH)
    else:
        GPIO.output("P8_10", GPIO.LOW)

    time.sleep(0.1)