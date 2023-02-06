/*
 * Author : Sara Messara - Clément Pagès 
 * Timestamp : 02.06.2023
 * Licence : BSD
 * 
 */


#include <DHT.h>
#include <SensorData.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <PubSubClient.h>

#define DHT_PIN  32 // ESP32 pin GIOP21 connected to DHT22 sensor
#define DHT_TYPE DHT22
#define PRESENCE_PIN 14
#define RANGE_TRIG_PIN 26
#define RANGE_ECHO_PIN 27

const char* mqtt_server = "51.178.50.237"; // mqtt config //
String types[] = {"f","f","f"};
long deltaT = 0;
long lastT = 0;
int value = 0;
WiFiClient espClient; // wifi config
PubSubClient client(espClient);
//
const char* ssid = "Sarsour";
const char* password = "cpldfpga49912";
//const char* ssid = "LarbiP";
//const char* password = "uuie1303";

DHT dht_sensor(DHT_PIN, DHT_TYPE); // humidity sensor
SensorData* test;
float distance_cm;
int pinStateCurrent = LOW;

void setup() {
  Serial.begin(9600);
  dht_sensor.begin(); // initialize the DHT sensor

  pinMode(RANGE_TRIG_PIN, OUTPUT);// set the Range sensor
  pinMode(RANGE_ECHO_PIN, INPUT);

  pinMode(PRESENCE_PIN, INPUT);// set the presence detector
  
  test = new SensorData(3,5,types,"Home", "ESP32");
  // network setup
  set_wifi(); // init wifi
  client.setServer(mqtt_server, 1883); // setting the server IP and Port
  client.setCallback(callback); // setting the MQTT callback function
  Serial.println("Finished Setup");
  while (!client.connected()) {
    reconnect();
    Serial.println("Connecting to MQTT broker");
  }
}


void set_wifi() {
  delay(10);
  
  // We start by connecting to a WiFi network
  Serial.println("Attempt");
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

//
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  //  // Feel free to add more if statements to control more GPIOs with MQTT
  //
  //  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off".
  //  // Changes the output state according to the message
  if (String(topic) == "esp32/output") {
    Serial.print("Changing output to ");
    if (messageTemp == "on") {
      Serial.println("on");
      //      digitalWrite(ledPin, HIGH);
    }
    else if (messageTemp == "off") {
      Serial.println("off");
      //      digitalWrite(ledPin, LOW);
    }
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("esp32/output");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void loop() {
  // read range
  deltaT = millis()- lastT;
  digitalWrite(RANGE_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(RANGE_TRIG_PIN, LOW);
  float duration_us = pulseIn(RANGE_ECHO_PIN, HIGH);
  // calculate the distance
  float rang = 0.017 * duration_us;
  //Serial.print("distance: ");
  //Serial.println(rang);

  // read humidity
  float humi  = dht_sensor.readHumidity();
  // read temperature in Celsius
  //Serial.print("humidity: ");
  //Serial.println(humi);
  float tempC = dht_sensor.readTemperature();
  // read temperature in Fahrenheit
  float tempF = dht_sensor.readTemperature(true);
  //Serial.print("temperature: ");
  Serial.println(tempC);

  // wait a 2 seconds between readings
  String here[] = {"Temperature", "Humidity", "Range"};
  float dataa[] = {tempC, humi, rang};
  test->dataSave(dataa, 3);
    // sending to MQTT broker
  if (deltaT >= 1000)
  {
    Serial.println("ccompute time");
    Serial.println(deltaT);
    DynamicJsonDocument jsonD = test->data2Json(here);
    String out("");
    //serializeJson(test->data2Json(here), out);
    serializeJson(jsonD, out);
    Serial.println("passing here");
    Serial.println(out);
    int n = out.length();
    char char_array[n + 1];
    strcpy(char_array, out.c_str());
    //out.toCharArray(output, 200);
    while (!client.connected()) 
    {
      reconnect();
      Serial.println("Connecting to MQTT broker");
    }
    client.publish("esp32/sensors",char_array);
    deltaT = 0;
    delete test;
    test = new SensorData(3,5,types,"home", "esp32"); // size of fifo 100 number of sensors 3
    lastT = millis();
  }
  int pinStatePrevious = pinStateCurrent; // store old state
  pinStateCurrent = digitalRead(PRESENCE_PIN);
  Serial.println(pinStateCurrent);
  if(pinStateCurrent == HIGH) //pinStatePrevious == LOW &&  
  {   
      char char_array[1];
      client.publish("esp32/presence",char_array);
  }
  delay(100);
}
