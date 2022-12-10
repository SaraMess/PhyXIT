#
#       
#
#

#========================================
#       Modules used in this file       
#========================================

import logging
import requests
import threading
import time

FREQ_MINUTES = 10

class VisualCrossingHandler(threading.Thread):
    """"""

    def __init__(self) -> None:
        threading.Thread.__init__(self)
        self.daemon = True
        self.citiesData = {"Toulouse" : [], "Alger" : []}


    def _performRequest(self, request : str) -> dict:
        """Perform request contained in string specified in argument and return the
        result provides by the weather API. This is a private function.
        ## Parameter :
        * request [in]: request to send to the weather API, as a string

        ## Return value :
        Dictionnary that contains API response to the specified request. This dictionnary
        can be empty if an error occured when querying the API"""

        logging.info(f"Sending request {request} to the weather API")
        response = requests.get(request)
        #If an error occured when querying weather API :
        if response.status_code != 200:
            logging.error(f"An error occured when querying weather API. Code error: {response.status_code}")
            return {}
        #Return received response in JSON format, in a dictionnary:
        responseJson = response.json()
        logging.debug(f"Response received: {responseJson}")
        return responseJson



    def currentWeatherRequest(self, locationName : str) -> dict:
        """Perform a request to the weather API to get current weather for specified location
        ## Parameter:
        * locationName [in]: name of the location whose we want know current weather

        ## Return:
        JSON response to the request, as a dictionnary"""
        
        current_weather_dict = {}
        keys_list = ["temp", "feelslike", "humidity", "precip", "precipprob", "precip", "windgust", "windspeed", "winddir", "pressure", "visibility", "cloudcover", "uvindex", "conditions", "stations"]
        logging.info(f"Performing a current weather request for {locationName}")
        request = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{locationName}/today?unitGroup=metric&include=current&key=S49E5MA43T843ZK2N6A4ZTT87&contentType=json&lang=id"
        response = self._performRequest(request)
        #If no response was received, return empty dict:
        if response == {}:
            return current_weather_dict
        response = response["currentConditions"]
        #Build current weather dict with needed data:
        for key in keys_list:
            try :
                current_weather_dict[key] = response[key]
            except KeyError as e:
                logging.error(e)
                current_weather_dict[key] = ""
        return current_weather_dict


    def add_city(self, location_name : str) -> int:
        """"""

        #Test if it is possible to add more city or not:
        if len(self.citiesData) == 6:
            logging.error("Limit for number of cities has been reached")
            return -1
        #Test if the specified location exists on VisualCrossing by performing a request
        #for this location
        if self.currentWeatherRequest(location_name) == {}:
            logging.error(f"An error occured while performing a request for {location_name}. \
            It seems that this city is not known by Visual Crossing API")
            return -2
        self.citiesData[location_name] = []
        return 0

    def run(self):
        #Run forever
        while True:
            #Get weather every 10 minutes
            time.sleep(60 * FREQ_MINUTES)
            current_time = time.localtime()
            logging.info(f"{current_time[3]}:{current_time[4]} ==> Getting weather data...")
            #Get weather data for each specified city:
            for city in self.citiesData:
                logging.info(f"Getting weather for {city}")
                current_data = self.currentWeatherRequest(city)
                logging.info(f"data strucutre received : {current_data}")
                #If there are less than 6 hours of data:
                if len(self.citiesData[city]) < 6 * (60 / FREQ_MINUTES):
                    self.citiesData[city].append(current_data)
                #Else remove the first sample, to keep 6 hours of data:
                else:
                    self.citiesData[city] = self.citiesData[city][1:].append(current_data)
            
