/*
   This ESP32 code is created by esp32io.com

   This ESP32 code is released in the public domain

   For more detail (instruction and wiring diagram), visit https://esp32io.com/tutorials/esp32-temperature-humidity-sensor
*/


#include <DHT.h>
#include <SensorData.h>
#include <ArduinoJson.h>
#include <WiFi.h>
#include <PubSubClient.h>

#define DHT_PIN  32 // ESP32 pin GIOP21 connected to DHT22 sensor
#define DHT_TYPE DHT22
#define PRESENCE_PIN 33
#define RANGE_TRIG_PIN 26
#define RANGE_ECHO_PIN 27

const char* mqtt_server = "51.178.50.237"; // mqtt config //
long lastMsg = 0;
char msg[50];
int value = 0;
int n1 =0;
int n2 = 0;
int n3 =0;
WiFiClient espClient; // wifi config
PubSubClient client(espClient);
//
const char* ssid = "Sarsour";
const char* password = "cpldfpga49912";
//const char* ssid = "LarbiP";
//const char* password = "uuie1303";

DHT dht_sensor(DHT_PIN, DHT_TYPE); // humidity sensor
SensorData test(3, 100);
float distance_cm;
int pass;

void setup() {
  Serial.begin(9600);
  Serial.println("In setup");
  dht_sensor.begin(); // initialize the DHT sensor

  pinMode(RANGE_TRIG_PIN, OUTPUT);// set the Range sensor
  pinMode(RANGE_ECHO_PIN, INPUT);

  pinMode(PRESENCE_PIN, INPUT);// set the presence detector

  float data[] = {1.1, 2.2, 3.3};
  test.dataSave(data, sizeof(data) / sizeof(data[0]));
  pass = -1;

  // network settup
  set_wifi(); // init wifi
  client.setServer(mqtt_server, 1883); // setting the server IP and Port
  client.setCallback(callback); // setting the MQTT callback function
  Serial.println("Finished Setup");

}


void set_wifi() {
  delay(10);
  
  // We start by connecting to a WiFi network
  Serial.println("Attempt");
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
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
n1 = n1 +1;
  n2 = n3= n1;
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
  String here[] = {"temp", "humi", "rang"};
  float dataa[] = {n1, n2, n3};
  test.dataSave(dataa, 3);
    // sending to MQTT broker
  if (!client.connected()) {
    reconnect();
    Serial.println("Connecting to MQTT broker");
  }

  //client.loop();
  //test.data2Json(here, output);
  Serial.println("output value");
  //Serial.println(output);
  //String str(output);
  //Serial.println(str);
  if (pass == 10)
  {
    DynamicJsonDocument jsonD = test.data2Json(here);
    String out("test");
    //serializeJson(test.data2Json(here), out);
    serializeJson(jsonD, out);
    Serial.println("passing here");
    //char* output = new char(200);
    Serial.println(out);
    int n = out.length();
    char char_array[n + 1];
    strcpy(char_array, out.c_str());
    Serial.println(char_array);
    //out.toCharArray(output, 200);
    client.publish("esp32/temperature",char_array);
    Serial.println(n);
    pass = -1;
  }
  else
    pass++;
  Serial.println("");
  delay(100);

}
