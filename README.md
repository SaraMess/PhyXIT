# PhyXIT
Physically eXtended Intereactive Technologies
PhyXIT is a hardware and software solution that allows the integration of both physical and virtual sensors, centralize the data on an online server and provide display by a graphical interface on Discord using a Discord Bot.  

The hardware application integrates 4 physical sensors (temperature, humidity, range and presence) wired to an ESP32 board. The communication to the online server was achieved using the MQTT protocol. The data were converted to Json objects before being published on the UPSSITECH broker @51.178.50.237 under the topic name "esp32/sensors".  

The software application is composed of 2 layers. The first layer integrates virtual sensors which retrieve the real time weather condition of a desired localisation obtained using Visual Crossing API. The second layer subscribes to the MQTT broker to retrieve the data collected by the ESP32 sensors. Finally, the display of data was made possible through a Discord Bot, which send data whenever requested by the user by commands. This solution combines both the benifits of sensors and API data centralisation as well as the functionnalities of the chat server.  

For the physical sensors, we imagined a scenario of house monitoring. We used indoor humidity and temperature sensors whose statistics can be used for instance to automatise the scheduling of the heating system of the house. The range sensor can be used to detect a near presence around a place, for instance, to prevent small children from getting close to dangerous places such as an operating stove or electrical outlets. Our solution is then suitable for domotic applications.
