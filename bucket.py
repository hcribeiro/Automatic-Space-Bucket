import sys
import time
import datetime
import RPi.GPIO as GPIO

LIGHT_PIN = 24

startTime = datetime.datetime.now().time()
endTime = (datetime.datetime.now() + datetime.timedelta(seconds=28800)).time()

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIGHT_PIN, GPIO.OUT)
    try:
        while(True):
            if (time_in_range(startTime, endTime, datetime.datetime.now().time())):
                GPIO.output(LIGHT_PIN, True)
                print("LED turned on!")
            elif not (time_in_range(startTime, endTime, datetime.datetime.now().time())):
                GPIO.output(LIGHT_PIN, False)
                print("LED turned off!")

            print("Time Now: " + str(datetime.datetime.now().time()))
            print("Start Time: " + str(startTime))
            print("End Time: " + str(endTime))
            time.sleep(10)
    finally:
        GPIO.cleanup()

def time_in_range(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime

if __name__ == "__main__":
    main()

