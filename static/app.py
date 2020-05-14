from flask import Flask, render_template, request
import sys, os, time, datetime, board, busio, yaml, threading
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import LED, DigitalOutputDevice, SmoothedInputDevice

config = []
dryness_threshold = -1

@app.route('/')
def index(humidity=0, light_status='Off', plant='N/a', logs=''):
    return render_template('dashboard.html', humidity=humidity, light_status=light_status, plant=plant, logs=logs)

def load_config():
    global dryness_threshold
    with open(os.path.expanduser("~/.bucket/config"), "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    return config

def time_in_range(startTime:time, endTime:time, nowTime:time) -> time:
    """Returns bool dependant on if nowTime is between startTime and endTime"""
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime

if __name__ == '__main__':
    global serverThread
    app = Flask(__name__)
    serverThread = threading.Thread(target=app.run, daemon=True)
    serverThread.start()
    config = load_config()
    difference = int(config['dryValue']) - int(config['wetValue'])
    dryness_threshold = int(config['dryValue']) - (difference * float(config['humidityThresh']))
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    led = LED(int(config['lightPin']), active_high=False)
    fans = DigitalOutputDevice(int(config['fanPin']), active_high=False)
    pumps = DigitalOutputDevice(int(config['pumpPin']), active_high=False)
    sensor = AnalogIn(ads, ADS.P0)
    startTime = datetime.datetime.now().time()
    endTime = (datetime.datetime.now() + datetime.timedelta(hours=float(config['sunHours']))).time()
    while(True):
        os.system('clear')
        now = datetime.datetime.now().time() 
        if (time_in_range(startTime, endTime, now)):
            led.on()
            fans.on()    
            # Read from sensor
            if (sensor.value > dryness_threshold):
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
        print("Threshold: " + str(dryness_threshold))
        time.sleep(10)
    serverThread.join()
