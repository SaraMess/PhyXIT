/*
   Authors : Sara Messara - Clement Pages
   Licence : BSD
   Stamped : 12:13 21.01.2023
   Part of the project PhyXIT
*/


#include <DHT.h>
#include <SensorData.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <PubSubClient.h>

#define DHT_PIN  32 // DHT22 sensor settings - humidity and temperature
#define DHT_TYPE DHT22 
#define PRESENCE_PIN 14 // MF-6402129 setting - presence 
#define RANGE_TRIG_PIN 26 // HC-SR settings - range 
#define RANGE_ECHO_PIN 27

const char* mqtt_server = "51.178.50.237"; // UPSSITECH mqtt broker
String types[] = {"f","f","f"}; // Specify sensors data type f-> floats i-> int b-> bool
long deltaT = 0;
long lastT = 0;
int value = 0;
WiFiClient espClient; // wifi config
PubSubClient client(espClient);

const char* ssid = "Sarsour";
const char* password = "cpldfpga49912"; // these are confidential clear data 

DHT dht_sensor(DHT_PIN, DHT_TYPE); // humidity sensor
SensorData* data_container;
float distance_cm;
int pinStateCurrent = LOW;

int numS = 3; // number of ensors
int sizeF = 10; // size of FIFO stack

void setup() {
  Serial.begin(9600);
  dht_sensor.begin(); // initialize the DHT sensor

  pinMode(RANGE_TRIG_PIN, OUTPUT);// set the Range sensor
  pinMode(RANGE_ECHO_PIN, INPUT);

  pinMode(PRESENCE_PIN, INPUT);// set the presence detector
  
  data_container = new SensorData(numS,sizeF,types,"Home", "ESP32"); 
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
  String messageTemp;
  for (int i = 0; i < length; i++) {
    messageTemp += (char)message[i];
  }
  //  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off".
  //  // Changes the output state according to the message
  if (String(topic) == "esp32/output") {
    if (messageTemp == "on") {
      //      digitalWrite(ledPin, HIGH);
    }
    else if (messageTemp == "off") {
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
  deltaT = millis()- lastT; // duration since last MQTT data sending
  digitalWrite(RANGE_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(RANGE_TRIG_PIN, LOW);
  float duration_us = pulseIn(RANGE_ECHO_PIN, HIGH);
  // calculate the distance
  float rang = 0.017 * duration_us;
  // read humidity
  float humi  = dht_sensor.readHumidity();
  float tempC = dht_sensor.readTemperature();
  // read temperature in Fahrenheit
  float tempF = dht_sensor.readTemperature(true);

  String here[] = {"Temperature", "Humidity", "Range"}; 
  float dataa[] = {tempC, humi, rang};
  data_container->dataSave(dataa, 3);
  
    // sending to MQTT broker
  if (deltaT >= 6000) // 600000
  {
    DynamicJsonDocument jsonD = data_container->data2Json(here);
    String out("");
    //serializeJson(data_container->data2Json(here), out);
    serializeJson(jsonD, out);
    int n = out.length();
    char char_array[n + 1];
    strcpy(char_array, out.c_str());
    //out.toCharArray(output, 200);
    while (!client.connected()) 
    {
      reconnect();
      Serial.println("Connecting to MQTT broker");
    }
    client.publish("esp32/sensors",char_array); // publishing on mqtt topic
    deltaT = 0;
    delete data_container;
    data_container = new SensorData(3,10,types,"Home", "Esp32"); // size of fifo 100 number of sensors 3
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
