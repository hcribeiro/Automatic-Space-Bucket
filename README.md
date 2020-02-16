# Automatic Space Bucket
Driver for RPI boards to control the environment inside a spacebucket. At the moment, the sofware can:
* Drive a powerful LED (through a transistor)
* Read Soil Humidity from a sensor
* Trigger a pump when Soil Humidity drops below a threshold
* Controls fans, turning on when the LED is on.

TODO:
* 3d files for Arduino and custom board
* Custom board design files
* Control PWM fans 
* Logic to disable LED if temperature reaches a certain level
