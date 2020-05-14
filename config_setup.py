import sys, os, time, board, busio, yaml
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

config = []

def main():
    if file_exists():
        with open(os.path.expanduser("~/.bucket/config"), "r") as config_file:
            config = yaml.load(config_file, Loader=yaml.BaseLoader)
        for item in config:
            if query_yes_no("Want to change the %s setting?" % str(item)):
                if "Value" in item:
                    config[item] = sensor_loop(item)
                else:
                    config[item] = query_string(item + " value:")
    else:
        config = first_setup()
        os.mkdir(os.path.expanduser('~/.bucket'))
    with open(os.path.expanduser("~/.bucket/config"), "w+") as config_file:
        yaml.dump(config, config_file)

def first_setup():
    temp_config = {}
    temp_config["dryValue"] = sensor_loop("dryValue")
    temp_config["wetValue"] = sensor_loop("wetValue")
    temp_config["hummidityThresh"] = query_string("Target Humidity %:")
    temp_config["lightPin"] = query_int("Pin for LED:")
    temp_config["fanPin"] = query_int("Pin for Fans:")
    temp_config["pumpPin"] = query_int("Pin for pump:")
    temp_config["plant"] = query_string("Plant Type:")
    temp_config["sunHours"] = query_string("# of Hours of Simulated Sunlight:")
    return temp_config

def file_exists():
    """ Checks if the config file exists with the right settings """
    if os.path.exists(os.path.expanduser('~/.bucket')):
        if os.path.isdir(os.path.expanduser('~/.bucket')):
            if os.path.exists(os.path.expanduser("~/.bucket/config")):
                return True
    return False

def sensor_loop(configType):
    """ Prompts user to prep sensor, then sets config value for matching configType """
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    sensor = AnalogIn(ads, ADS.P0)
    try:
        while(True):
            os.system('clear')
            print("Setting %s value:" % configType)
            print("Sensor: " + str(sensor.value))
            print("Ctrl + C to stop")
            time.sleep(.5)
    except KeyboardInterrupt:
        os.system('clear')
        print("Averaging input...")
        count=0
        sum=0
        while(count < 10):
            sum += sensor.value
            count +=1
            time.sleep(.5)
        os.system('clear')
        print("%s value: %d" % (configType, sum/10))
        return sum/10

def query_yes_no(question:str, default:str="yes") -> bool:
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    Source:
    https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def query_string(question:str) -> str:
    """Ask a simple question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    """
    sys.stdout.write(question)
    return input().lower()

def query_int(question:str) -> int:
    """Ask a simple question via raw_input() and return their answer, if valid int.

    "question" is a string that is presented to the user.
    """

    while True:
        sys.stdout.write(question)
        try:
            return int(input())
        except ValueError:
            sys.stdout.write("Please respond with a only numerical input.\n")

if __name__ == "__main__":
    main()