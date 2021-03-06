import sys, os, time, datetime, board, busio, yaml
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import LED, DigitalOutputDevice, SmoothedInputDevice

LIGHT_PIN = 26
FANS_PIN = 20
PUMP_PIN = 21

startTime = datetime.datetime.now().time()
endTime = (datetime.datetime.now() + datetime.timedelta(hours=23.5)).time()

def main():
    DRYNESS_THRESHOLD = load_config()
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    led = LED(LIGHT_PIN, active_high=False)
    fans = DigitalOutputDevice(FANS_PIN, active_high=False)
    pumps = DigitalOutputDevice(PUMP_PIN, active_high=False)
    sensor = AnalogIn(ads, ADS.P0)
    while(True):
        os.system('clear')
        now = datetime.datetime.now().time() 
        if (time_in_range(startTime, endTime, now)):
            led.on()
            fans.on()    
            # Read from sensor
            if (sensor.value > DRYNESS_THRESHOLD):
                pumps.on()
                print("Pump turned on!")
            else:
                pumps.off()
                print("Pump turned off!")
            print("LED turned on!")
        elif not (time_in_range(startTime, endTime, now)):
            led.off()
            fans.off()
            print("LED turned off!")
        print("Time Now: " + str(now))
        print("Start Time: " + str(startTime))
        print("End Time: " + str(endTime))
        print("Sensor: " + str(sensor.value))
        print("Threshold: " + str(DRYNESS_THRESHOLD))
        time.sleep(10)

def load_config():
    config = []
    with open(os.path.expanduser("~/.bucket/config"), "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    difference = int(config['dryValue']) - int(config['wetValue'])
    return int(config['dryValue']) - (difference * .4) # going for 40%

def time_in_range(startTime:time, endTime:time, nowTime:time) -> time:
    """Returns bool dependant on if nowTime is between startTime and endTime"""
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime

if __name__ == "__main__":
    main()

