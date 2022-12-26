#**************************************************#
#       Visual Crossing Handler Module File        #
#**************************************************#
#   Authors : Sara MESSARA - Clément PAGES         #
#**************************************************#


#========================================#
#       Modules used in this file        #
#========================================#

import logging
import os
import requests



def _performRequest(request : str) -> dict:
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


def currentWeatherRequest(locationName : str) -> dict:
    """Perform a request to the weather API to get current weather for specified location
    ## Parameter:
    * `locationName`: name of the location whose we want know current weather
    ## Return value:
    JSON response to the request, as a dictionnary. If an error occured, this
    dict is empty"""

    current_weather_dict = {}
    keys_list = ["temp", "feelslike", "humidity", "precip", "precipprob", "preciptype", "precip", "windgust", "windspeed", "winddir", "pressure", "visibility", "cloudcover", "uvindex", "conditions", "stations"]
    logging.info(f"Performing a current weather request for {locationName}")
    request = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{locationName}/today?unitGroup=metric&include=current&key={os.environ['VC_TOKEN']}&contentType=json&lang=id"
    response = _performRequest(request)
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
