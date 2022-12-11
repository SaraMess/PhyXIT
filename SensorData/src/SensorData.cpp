#include"SensorData.h"


SensorData::SensorData(int sSize, int fSize):sSize(sSize), fSize(fSize) {
    data = new Fifo<float>*[sSize];
    types = new int[sSize];
    for(int i=0;i<sSize; i++)
    {
        data[i] = new Fifo<float>(fSize);
        types[i] = 0;
        //std::cout<<sizeof(data[i])<<std::endl;
    }
    dataJson = dataJson.to<JsonObject>();
    dataJson["Server"] = "ESP32";
    dataJson["Localisation"] = "Home";

    levels = new JsonObject[sSize];
    for(int i=0; i<sSize;i++)
    {
        levels[i] = root.createNestedObject("Sensor"+String(i));
    }

    } 
SensorData::SensorData(int sSize, int fSize, string server, string localisation):sSize(sSize), fSize(fSize) {
    data = new Fifo<float>*[sSize];
    types = new int[sSize];
    for(int i=0;i<sSize; i++)
    {
        data[i] = new Fifo<float>(fSize);
        types[i] = 0;
        //std::cout<<sizeof(data[i])<<std::endl;
    }
    dataJson = dataJson.to<JsonObject>();
    dataJson["Server"] = server;
    dataJson["Localisation"] = localisation;
    } 

SensorData::SensorData(int sSize, int fSize, int* typ):sSize(sSize), fSize(fSize) {
    data = new Fifo<float>*[sSize];
    types = new int[sSize];
    for(int i=0;i<sSize; i++)
    {
        data[i] = new Fifo<float>(fSize);
        types[i] = typ[i];
        //std::cout<<sizeof(data[i])<<std::endl;
    }
    } 
SensorData::SensorData(int sSize, int fSize, int* typ, string server, string localisation):sSize(sSize), fSize(fSize) {
    data = new Fifo<float>*[sSize];
    types = new int[sSize];
    for(int i=0;i<sSize; i++)
    {
        data[i] = new Fifo<float>(fSize);
        types[i] = typ[i];
        //std::cout<<sizeof(data[i])<<std::endl;
    }
    dataJson = dataJson.to<JsonObject>();
    dataJson["Server"] = server;
    dataJson["Localisation"] = localisation;
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
  }
  
  int SensorData::dataSave(float* D, int sizeD)
  {
    try {
    if (sizeD>= sSize) {
        //std::cout << "Saving data to FIFO."<<std::endl;
        for(int i=0;i<sSize; i++)
            {   
                //std::cout<<i<<std::endl;
                (data[i])->push_back(D[i]);
                //std::cout<<"data "<<i <<" "<< (data[i])->front()<<std::endl;
            }
            return 1;
    } 
    else {
        throw (0);
        }
    }
    catch (int myNum) {
       // std::cout << "Not enough data. No recording."<<std::endl;
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

int SensorData::data2Json(string* fieldName)
{
    
    
    for(int i=0;i<sSize;i++)
    {  
        levels2 = level1.createNestedArray(fieldName[i]);
        while(!(data[i])->isEmpty())
        {
            levels2.add((data[i])->front());
            (data[i])->pop_front();
        }
        
    }
    serializeJson(dataJson, Serial);
    return 1;
}