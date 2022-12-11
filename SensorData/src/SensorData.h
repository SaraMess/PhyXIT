#ifndef __SensorData__
#define __SensorData__

/** \brief Fifo Optimised fixed size at creation FIFO template for embedded programming.
     *
     *  Container that allows the controll of the
     * Fifo size at creation, thus suitable for memory management.
     * Upgrade of the C++ std stack and queue.
     */
#include <memory>
#include <stdio.h>      /* printf, scanf, NULL */
#include <stdlib.h>     
#include "ArduinoJson.h"
#include "Arduino.h"
#include <string>
#include <iostream>

   template<typename T>
    class Fifo
    {
        private:
        int max_size;
        std::unique_ptr<T[]> data;
        int c_size;
        int index_write;
        int index_read;
        
        public:

        /** dynamic fixed size allocation 
         * enable the control of the FIFO size,
         * suitable for embedded programming
         */
        /*
        Fifo(): max_size(100), data(new T[100])
        {}*/
        Fifo(int size): max_size(size), data(new T[size])
        {
            index_write= -1;
            index_read = -1;
            c_size = 0;
        }

        Fifo(const Fifo & another) = delete;

        /** append a new value to the FIFO
         */
        void push_back(T another) noexcept
        {
            if (index_write<0)
            {
                index_write = ( index_write + 1) % max_size;
                data[index_write] = another;
                c_size = c_size + 1;
            }
            else
            {
                index_write = (index_write + 1) % max_size;
                if(index_read == index_write)
                    index_read = (index_read + 1) % max_size;
                data[index_write] = another;
                c_size = c_size + 1; 
                if (c_size>max_size) 
                    c_size = max_size;
            }
        }

        /** test if the FIFO is empty
         */
        bool isEmpty(void)
        {
            return  (c_size == 0);
        }

        /** delete the oldest value, 
         * move the reading index forward
         */
        void pop_front(void)
        {
            if(index_read < 0) 
                index_read = 0;
            if(!this->isEmpty())
            {
                index_read = (index_read + 1) % max_size;
                c_size--;
            }
        }

        /** return the oldest value inserted in the FIFO,
         * without moving the reading index
         */
        T& front(void)
        {   
            if(index_read<0) 
                index_read=0;
            if(!this->isEmpty())
                return data[index_read];
            else 
                return data[0];
        }

        /** return the newest value inserted in the FIFO,
         * without moving the reading index
         */
        T& back(void)
        {   
            if(!this->isEmpty())
            return data[index_write];
            else
            return data[0];
        }
        /** return the current size of the FIFO
         */
        int size(void)
        {   
            return c_size;
        }

        void reset(void)
        {
            index_read = index_write = 0;
            c_size = 0;
        }


        T& operator[](int index)
        {
            if(index>=max_size || index<0)
            return front();
            else
            return data[index];
        }

        T& operator=(T& value) = delete;
    };


class SensorData{
    int sSize;
    int fSize;
    //Fifo<float>* data;
    //Fifo<float> rang;
    //Fifo<float> humi;
    //Fifo<float> temp;
    //Fifo<float> dete;
    Fifo<float>** data; // all the sensors
    int* types;
    StaticJsonDocument<10000> dataJson; // check if viable
    JsonObject* levels; // sensors group
    
    public:
    SensorData(int, int, int*);
    SensorData(int, int, int*, string, string)
    SensorData(int sSize, int fSize);
    SensorData(int, int, string, string)
    SensorData(int);
    SensorData();
    ~SensorData();
    int dataSetSize(int fSize);
    void dataSend(void);
    int dataSave(float*, int);
    int dataSave(float*, int, int*);
    int data2Json(void);

};


#endif