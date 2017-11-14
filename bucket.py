import sys
import time
import datetime
import RPi.GPIO as GPIO
from pi_sht1x import SHT1x
from Adafruit_IO import MQTTClient

ADAFRUIT_IO_KEY      = 'ac26e7416eca340d38620c50e4bb107ffeadd001'
ADAFRUIT_IO_USERNAME = 'Blabermouthe'

DATA_PIN = 18
SCK_PIN = 23
LIGHT_PIN = 24


def connected(client):
    print('Connected to Adafruit IO!  Listening for feed changes...')
    client.subscribe('temperature')
    client.subscribe('humidity')

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message


startTime = datetime.datetime.now().time()
endTime = (datetime.datetime.now() + datetime.timedelta(seconds=28800)).time()
ledStatus = False
lastStatus = False

def main():
    global lastStatus
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LIGHT_PIN, GPIO.OUT)
    try:
        while(True):
            #if (not client.is_connected()):
                #client.connect()
                #client.loop_background()
            # Read from sensor
            # sensor = SHT1x(DATA_PIN, SCK_PIN, gpio_mode=GPIO.BCM)
            # temp = sensor.read_temperature()
            # humidity = sensor.read_humidity(temp)
            # print(sensor)

            # Stream data to Adafruit
            # client.publish('temperature', temp)
            # client.publish('humidity', humidity)

            if (time_in_range(startTime, endTime, datetime.datetime.now().time())):
                GPIO.output(LIGHT_PIN, True)
                print("LED turned on!")
            elif not (time_in_range(startTime, endTime, datetime.datetime.now().time())):
                GPIO.output(LIGHT_PIN, False)
                print("LED turned off!")

            print("Time Now: " + str(datetime.datetime.now().time()))
            print("Start Time: " + str(startTime))
            print("End Time: " + str(endTime))
            print("Last Status: " + str(lastStatus))
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

