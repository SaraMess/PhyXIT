#**************************************************#
#       Visual Crossing Handler Class File         #
#**************************************************#
#   Authors : Sara MESSARA - Clément PAGES         #
#**************************************************#


#========================================#
#       Modules used in this file        #
#========================================#

import logging
import requests
import threading
import time



FREQ_MINUTES = 10


#===============================#
#       Class Declaration       #
#===============================#

class VisualCrossingHandler(threading.Thread):
    """Class allowing the management of requests to the Visual Crossing weather
    API. In particular, this class executes a thread whose objective is to send
    at regular intervals a request for all the cities specified by the user, within
    the limit of 6 cities. This last constraint is linked to the use of a free account
    to access the Visual Crossing data, which limits the use of the API to 1000 requests
    per day"""

    def __init__(self) -> None:
        """Class constructor"""

        threading.Thread.__init__(self)
        self.daemon = True
        self.citiesData = {"Toulouse" : [], "Alger" : []}


    def _performRequest(self, request : str) -> dict:
        """Perform request contained in string specified in argument and return the
        result provided by the weather API. This is a private method.
        ## Parameter :
        * `request`: request to send to the weather API, as a string
        ## Return value :
        Dictionnary that contains API response for the specified request. This
        dictionnary can be empty if an error occured when querying the API"""

        logging.info(f"Sending request {request} to the weather API")
        response = requests.get(request)
        #If an error occured when querying weather API return an empty dict:
        if response.status_code != 200:
            logging.error(f"An error occured when querying weather API. Error code: {response.status_code}")
            return {}
        #Return received response in JSON format, as a dictionnary:
        responseJson = response.json()
        logging.debug(f"Response received: {responseJson}")
        return responseJson


    def currentWeatherRequest(self, locationName : str) -> dict:
        """Perform a request to the weather API to get current weather for specified location
        ## Parameter:
        * `locationName`: name of the location whose we want know current weather
        ## Return value:
        JSON response to the request, as a dictionnary. If an error occured, this
        dict is empty"""

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
        """Add a city for which the bot should get the current weather from the
        Visual Crossing API. Because of the free account limit of 1000 requests
        per day, the maximum number of cities is set to 6.
        ## Parameters:
        * `location_name`: name of the location to add to the cities list
        ## Return value:
        * `0` if the city have been successfully added to the cities list
        * `-1` if the city cannot be added because limit of number of cities
        has been reached
        * `-2` if the specified city does not exist in the Visual Crossing database"""

        #Test if it is possible to add one more city:
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
        """Redefinition of the `run` method of the `Thread` class. This function
        performs a query of the current weather for all the cities specified by
        the user, at a frequency of `FREQ_MINUTES`"""

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
