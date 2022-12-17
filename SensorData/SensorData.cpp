#include"SensorData.h"


SensorData::SensorData(int sSize, int fSize):sSize(sSize), fSize(fSize), dataJson(10000) {
    data = new Fifo<float>*[sSize];
    types = new int[sSize];
    for(int i=0;i<sSize; i++)
    {
        data[i] = new Fifo<float>(fSize);
        types[i] = 0;
    }
    dataJson = dataJson.to<JsonObject>();
    dataJson["Server"] = "ESP32";
    dataJson["Localisation"] = "Home";
    levels = dataJson.createNestedObject("Sensors");
    } 
SensorData::SensorData(SensorData &other):dataJson(1000) {
    sSize = other.sSize;
    fSize = other.fSize;
    data = new Fifo<float>*[sSize];
    types = new int[sSize];
    for(int i=0;i<sSize; i++)
    {
        data[i] = new Fifo<float>(fSize);
        types[i] = 0;
    }
    dataJson = dataJson.to<JsonObject>();
    dataJson["Server"] = "ESP32";
    dataJson["Localisation"] = "Home";
    levels = dataJson.createNestedObject("Sensors");
    } 

SensorData::SensorData(int sSize, int fSize, String server, String localisation):sSize(sSize), fSize(fSize),dataJson(10000) {
    data = new Fifo<float>*[sSize];
    types = new int[sSize];
    for(int i=0;i<sSize; i++)
    {
        data[i] = new Fifo<float>(fSize);
        types[i] = 0;
    }
    dataJson = dataJson.to<JsonObject>();
    dataJson["Server"] = server;
    dataJson["Localisation"] = localisation;
    levels = dataJson.createNestedObject("Sensors");
    } 

SensorData::SensorData(int sSize, int fSize, int* typ):sSize(sSize), fSize(fSize),dataJson(10000) {
    data = new Fifo<float>*[sSize];
    types = new int[sSize];
    for(int i=0;i<sSize; i++)
    {
        data[i] = new Fifo<float>(fSize);
        types[i] = typ[i];
    }
    } 
SensorData::SensorData(int sSize, int fSize, int* typ, String server, String localisation):sSize(sSize), fSize(fSize),dataJson(10000) {
    data = new Fifo<float>*[sSize];
    types = new int[sSize];
    for(int i=0;i<sSize; i++)
    {
        data[i] = new Fifo<float>(fSize);
        types[i] = typ[i];
    }
    dataJson = dataJson.to<JsonObject>();
    dataJson["Server"] = server;
    dataJson["Localisation"] = localisation;
    levels = dataJson.createNestedObject("Sensors");
    } 
/*SensorData::SensorData(int sSize, int fSize, int* types):sSize(sSize), fSize(fSize) {
    data = new Fifo<float>*[sSize];
    for(int i=0;i<sSize; i++)
    {   switch(types[i]){
        case 0:
            data[i] = new Fifo<float>(fSize);
            std::cout<<sizeof(data[i])<<std::endl;
            break;
        case 1:
            data[i] = new Fifo<bool>(fSize);
            std::cout<<sizeof(data[i])<<std::endl;
        case 2:
            data[i] = new Fifo<int>(fSize);
            std::cout<<sizeof(data[i])<<std::endl;
        default:
            break;
    }
    }
    } */
  SensorData::~SensorData(){
    for(int i=0;i<sSize; i++)
    {
        delete data[i];
    }
    delete[] data;
    delete[] types;
  }
  
  int SensorData::dataSave(float* D, int sizeD)
  {
    try {
    if (sizeD>= sSize) {
        for(int i=0;i<sSize; i++)
            {   
                (data[i])->push_back(D[i]);
            }
            return 1;
    } 
    else {
        throw (0);
        }
    }
    catch (int myNum) {
        return 0;
    }
  }

   /*int SensorData::dataSave(float* D, int sizeD, int types)
  {
    try {
    if (sizeD>= sSize) {
        std::cout << "Saving data to FIFO."<<std::endl;
        for(int i=0;i<sSize; i++)
            {   
                switch(types[i]){
                    case 0:
                        std::cout<<i<<std::endl;
                        (data[i])->push_back((float)D[i]);
                        std::cout<<"data "<<i <<" "<< (data[i])->front()<<std::endl;
                        break;
                    case 1:
                        std::cout<<i<<std::endl;
                        (data[i])->push_back((bool)D[i]);
                        std::cout<<"data "<<i <<" "<< (data[i])->front()<<std::endl;
                        break;
                    case 2:
                        std::cout<<i<<std::endl;
                        (data[i])->push_back((int)D[i]);
                        std::cout<<"data "<<i <<" "<< (data[i])->front()<<std::endl;
                        break;
                    default:
                        break;
                }
            }
            return 1;
        }
        
    else {
        throw (0);
        }
    }
    catch (int myNum) {
        std::cout << "Not enough data. No recording."<<std::endl;
        return 0;
    }
  }*/
/*
int SensorData::data2Json(String* fieldName)
{
    
    
    for(int i=0;i<sSize;i++)
    {  
        JsonArray levels2 = levels.createNestedArray(fieldName[i]);
        while(!(data[i])->isEmpty())
        {
            levels2.add((data[i])->front());
            (data[i])->pop_front();
        }
        
    }
    serializeJsonPretty(dataJson, Serial);
    return 1;
}*/
int SensorData::data2Json(String* fieldName, char* output)
{
    for(int i=0;i<sSize;i++)
    {  
        JsonArray levels2 = levels.createNestedArray(fieldName[i]);
        while(!(data[i])->isEmpty())
        {
            levels2.add((data[i])->front());
            Serial.println("in sensorData");
            Serial.println((data[i])->front());
            (data[i])->pop_front();
        }
        
    }
    serializeJson(dataJson, output, sizeof(output));
    return 1;
}

DynamicJsonDocument SensorData::data2Json(String* fieldName)
{
    for(int i=0;i<sSize;i++)
    {  
        JsonArray levels2 = levels.createNestedArray(fieldName[i]);
        while(!(data[i])->isEmpty())
        {
            levels2.add((data[i])->front());
            Serial.println("in sensorData");
            Serial.println((data[i])->front());
            (data[i])->pop_front();
        }
    }
    return dataJson;
}