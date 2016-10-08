
#include <Chrono.h>

#include "Wire.h"
#include <LiquidCrystal.h>

// Include Sensirion library
#include <Sensirion.h>


// Sensor pins
const uint8_t dataPin = 6;
const uint8_t clockPin = 7;
//const uint8_t fanPin = 3;
const int lightPin = 11;
const uint8_t buttonPin = 2;
const int screenPin =  13;

// Variables
float temperature;
float humidity;
float dewpoint;
int buttonState = 0;
int displayMode = 0;
int hours = 10;
//int fanVal = 0;
unsigned long lastPress;
Chrono startTime(Chrono::SECONDS); 
bool ledStatus = true;


Sensirion soilSensor = Sensirion(dataPin, clockPin);
LiquidCrystal lcd(0);

void setup() 
{
  pinMode(buttonPin, INPUT);
  pinMode(screenPin, OUTPUT);
  //pinMode(fanPin, OUTPUT);
  
  /*lcd.begin(16, 2);
  lcd.setBacklight(HIGH);
  lastPress = millis();*/

  pinMode(lightPin, OUTPUT);
  digitalWrite(lightPin, HIGH);
  
  // Start timer
  startTime.restart();
  
  //Serial.begin(9600);
  //Serial.println("Started!");

}

void loop() 
{
  // Take measurement
  //soilSensor.measure(&temperature, &humidity, &dewpoint);
  //buttonState = digitalRead(buttonPin);
  
  // 18 hours on and 8 hours off
  if((ledStatus && startTime.hasPassed(hours*3600)) || (!ledStatus && startTime.hasPassed((24-hours)*3600)))
  {
    ledStatus = !ledStatus;
    startTime.restart();
  }

  /*if(displayMode == 0)
  {
    lcd.setCursor(0, 0);
    lcd.print("Temperature:");
    lcd.setCursor(0, 1);
    lcd.print(temperature);
    lcd.print(" C");
  }
  else
  {
    lcd.setCursor(0, 0);
    lcd.print("Humidity:");
    lcd.setCursor(0, 1);
    lcd.print(humidity);
    lcd.print(" %");
  }

  if (buttonState == HIGH) {
    if((millis() - lastPress) < 10000)
    {
      lcd.clear();
      displayMode = 1 - displayMode;
    }
    lastPress = millis();
  } 

  if((millis() - lastPress) < 10000)
  {
    lcd.display();
    lcd.setBacklight(HIGH);
  }
  else
  {
    lcd.noDisplay();
    lcd.setBacklight(LOW);
  }*/

  // FAN Stuff
  //analogWrite(fanPin, fanVal);
  //fanVal += 10;
  //if(fanVal > 255)
  //{
  //  fanVal = 0;
  //}

  if(ledStatus)
  {
    digitalWrite(lightPin,HIGH);
  }
  else
  {
    digitalWrite(lightPin, LOW);
  }

  //Serial.println(startTime.elapsed());
  
  // Wait 100 ms before next measurement
  delay(100);  
}
