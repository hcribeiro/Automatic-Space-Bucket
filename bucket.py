import sys, os, time, datetime
from gpiozero import LED, DigitalOutputDevice, SmoothedInputDevice

LIGHT_PIN = 26
FANS_PIN = 20
PUMP_PIN = 21
SENSOR_PIN = 16

startTime = datetime.datetime.now().time()
endTime = (datetime.datetime.now() + datetime.timedelta(hours=23)).time()

def main():
    led = LED(LIGHT_PIN, active_high=False)
    fans = DigitalOutputDevice(FANS_PIN, active_high=False)
    pumps = DigitalOutputDevice(PUMP_PIN, active_high=False)
    while(True):
        os.system('clear')
        now = datetime.datetime.now().time() 
        if (time_in_range(startTime, endTime, now)):
            led.on()
            fans.on()
            print("LED turned on!")
            print("Time Now: " + str(now))
            print("Start Time: " + str(startTime))
            print("End Time: " + str(endTime))
        elif not (time_in_range(startTime, endTime, now)):
            led.off()
            fans.off()
            print("LED turned off!")
            print("Time Now: " + str(now))
            print("Start Time: " + str(startTime))
            print("End Time: " + str(endTime))
        time.sleep(10)

def time_in_range(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime

if __name__ == "__main__":
    main()

