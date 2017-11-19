# Automatic Space Bucket
Driver for Arduino boards to control the environment inside a spacebucket. At the moment, the sofware can:
* Drive a powerful LED (through a transistor)
* Control PWM fans (currently commented out)
* Read Temperature/Humidity from a soil sensor
* Control a display, display turns off when not in use, a button toggles between Temperature and Humidity output

TODO:
* 3d files for Arduino and custom board
* Custom board design files
* Wifi module to output current values to a server (maybe)
* Logic to disable LED if temperature reaches a certain level
* Logic to switch between modes for different plants
* Pump to add water (maybe)
