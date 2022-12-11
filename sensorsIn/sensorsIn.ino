/*
 * This ESP32 code is created by esp32io.com
 *
 * This ESP32 code is released in the public domain
 *
 * For more detail (instruction and wiring diagram), visit https://esp32io.com/tutorials/esp32-temperature-humidity-sensor
 */


#include <DHT.h>
#include <SensorData.h>
#include <ArduinoJson.h>
#define DHT_PIN  32 // ESP32 pin GIOP21 connected to DHT22 sensor
#define DHT_TYPE DHT22
#define PRESENCE_PIN 33
#define RANGE_TRIG_PIN 26
#define RANGE_ECHO_PIN 27


DHT dht_sensor(DHT_PIN, DHT_TYPE);
SensorData test(3,10);
float distance_cm;
int pass;

void setup() {
  Serial.begin(9600);
  dht_sensor.begin(); // initialize the DHT sensor
  
  pinMode(RANGE_TRIG_PIN, OUTPUT);// set the Range sensor
  pinMode(RANGE_ECHO_PIN, INPUT);
  
  pinMode(PRESENCE_PIN, INPUT);// set the presence detector
  
  float data[] ={1.1,2.2,3.3};
  test.dataSave(data,sizeof(data)/sizeof(data[0]));
  pass = 0;


}

void loop() {

  // read range
  digitalWrite(RANGE_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(RANGE_TRIG_PIN, LOW);
  float duration_us = pulseIn(RANGE_ECHO_PIN, HIGH);
  // calculate the distance
  float rang = 0.017 * duration_us;
  Serial.print("distance: ");
  Serial.println(rang);
  
  // read humidity
  float humi  = dht_sensor.readHumidity();
  // read temperature in Celsius
  Serial.print("humidity: ");
  Serial.println(humi);
  float tempC = dht_sensor.readTemperature();
  // read temperature in Fahrenheit
  float tempF = dht_sensor.readTemperature(true);
  Serial.print("temperature: ");
  Serial.println(tempC);

  // wait a 2 seconds between readings
  String here[] = {"hum","temp","range"};
  float dataa[] = {tempC,humi,rang};
  test.dataSave(dataa, 3);
  if(pass == 3)
    {
      test.data2Json(here);
      pass=-1;
    }
  else 
    pass++;
  Serial.println("");
  delay(4000);
}
