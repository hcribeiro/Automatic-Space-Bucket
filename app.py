from flask import Flask, render_template, request
import sys, os, time, datetime, board, busio, yaml, threading, logging
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import LED, DigitalOutputDevice, SmoothedInputDevice

config = []
dryness_threshold = -1
app = Flask("SpaceBucket")

@app.route('/')
def index(light_status='Off', plant='N/a', logs=''):
    plant = config['plant']
    now = datetime.datetime.now().time() 
    if (time_in_range(startTime, endTime, now)):
        light_status = 'On'
    elif not (time_in_range(startTime, endTime, now)):
        light_status = 'Off'
    return render_template('dashboard.html', humidity=humidity, threshold=dryness_threshold, light_status=light_status, startTime=startTime, endTime=endTime, plant=plant, logs=logs)

def load_config():
    with open(os.path.expanduser("~/.bucket/config"), "r") as config_file:
        config = yaml.load(config_file, Loader=yaml.BaseLoader)
    return config

def time_in_range(startTime:time, endTime:time, nowTime:time) -> bool:
    """Returns bool dependant on if nowTime is between startTime and endTime"""
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARN)
    logger.addHandler(ch)

    global humidity, startTime, endTime
    serverThread = threading.Thread(target=app.run, daemon=True, kwargs={'host':'0.0.0.0'})
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
        humidity = sensor.value
        now = datetime.datetime.now().time() 
        if (time_in_range(startTime, endTime, now)):
            led.on()
            fans.on()
            logger.info("LED turned on!")
        elif not (time_in_range(startTime, endTime, now)):
            led.off()
            fans.off()
            logger.info("LED turned off!")
        if (sensor.value > dryness_threshold):
            pumps.on()
            logger.info("Pump turned on!")
        else:
            pumps.off()
            logger.info("Pump turned off!")
        logger.debug("Time Now: " + str(now))
        logger.debug("Start Time: " + str(startTime))
        logger.debug("End Time: " + str(endTime))
        logger.debug("Sensor: " + str(sensor.value))
        logger.debug("Threshold: " + str(dryness_threshold))
        time.sleep(10)
    serverThread.join()
