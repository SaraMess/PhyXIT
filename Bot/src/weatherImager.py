#**************************************************#
#           weather imager Module File             #
#**************************************************#
#   Authors : Sara MESSARA - Clément PAGES         #
#**************************************************#


#========================================#
#       Modules used in this file        #
#========================================#

from weather import *
from Image import *


#========================================#
#       Constants declaration            #
#========================================#

#Constants for image generation:
FONT_PATH = "./data/font/Ubuntu-R.ttf"
BIG_FONT_SIZE =     80
MEDIUM_FONT_SIZE =  40
SMALL_FONT_SIZE =   20

BIG_FONT     = font.truetype(FONT_PATH, BIG_FONT_SIZE)
MEDIUM_FONT  = font.truetype(FONT_PATH, MEDIUM_FONT_SIZE)
SMALL_FONT   = font.truetype(FONT_PATH, SMALL_FONT_SIZE)

ICON_SIZE =         (50, 50)

LEFT_ALIGNMENT = 20
CENTRE_ALIGNMENT = 320
UP_ALIGNMENT = 10
INTER_ALIGNMENT = 30
MIN_MAX_TEMP_ALIGNMENT = UP_ALIGNMENT + BIG_FONT_SIZE + 10
ITEMS_UP_ALIGNMENT = MIN_MAX_TEMP_ALIGNMENT + MEDIUM_FONT_SIZE + INTER_ALIGNMENT
TXT_VERTICAL_ALIGNMENT = LEFT_ALIGNMENT + ICON_SIZE[0] + INTER_ALIGNMENT
TXT_CENTRAL_VERTICAL_ALIGNMENT = CENTRE_ALIGNMENT + ICON_SIZE[0] + INTER_ALIGNMENT
TXT_HORIZONTAL_ALIGNMENT = 10

MAIN_ICON_SIZE = (MIN_MAX_TEMP_ALIGNMENT + MEDIUM_FONT_SIZE, MIN_MAX_TEMP_ALIGNMENT + MEDIUM_FONT_SIZE)
ITEM_HEIGHT = ICON_SIZE[1] + INTER_ALIGNMENT



def _generate_weather_image(weather_condition_code : str) -> Image:
    """Generate a basic image with adapted background and weather icon according 
    to the specified weather condition code
    ## Parameter:
    * `weather_condition_code` : weather conditon code, as a string
    ## Return value:
    Return basic image with adapted background. This image can be used to add
    elements on top of it"""

    #Create background image according to current weather conditions:
    weather_image = Image(get_path_image_weather_type(weather_condition_code))
    #Add mask to the image:
    weather_image.addMask("BLACK", 180, (weather_image.width // 2 + 40, weather_image.height), (0, 0))
    #Add weather icon according to current weather:
    weather_image.addIcon(get_icon_path_weather_type(weather_condition_code), MAIN_ICON_SIZE, (350, UP_ALIGNMENT))
    weather_image.addIcon(f"{ICON_DIR_PATH}logoVC.jpeg", ICON_SIZE, (5, weather_image.height - 45))
    weather_image.drawText("Données de l'API VisualCrossing", SMALL_FONT, (60, weather_image.height - 40))
    return weather_image


def _add_precip_data(request_response : dict, weather_image : Image) -> Image :
    """Add precipitation information contained in JSON request response to the
    specified `weather_image`
    ## Parameters:
    * `request_response`: JSON response to the request, as a dict
    * `weather_image`: image where add precipitations data
    ## Return value:
    Weather image with added precipitations data, for chained calls"""

    #If excepted precipitation type is rain, freezing or ice:
    if request_response['preciptype'] in ['rain', 'freezing', 'ice']:
        weather_image.addIcon(f"{ICON_DIR_PATH}water-drop.png", ICON_SIZE, (LEFT_ALIGNMENT, ITEMS_UP_ALIGNMENT))
        weather_image.drawText(f"{request_response['precipprob']}%", MEDIUM_FONT, (TXT_VERTICAL_ALIGNMENT, ITEMS_UP_ALIGNMENT))
        weather_image.addIcon(f"{ICON_DIR_PATH}pluviometer.png", ICON_SIZE, (CENTRE_ALIGNMENT, ITEMS_UP_ALIGNMENT))
        precip = request_response['precip']
        if precip > 0.:
            weather_image.drawText(f"{precip}mm", MEDIUM_FONT, (TXT_CENTRAL_VERTICAL_ALIGNMENT, ITEMS_UP_ALIGNMENT))
    #If excepted precipitation type is snow:
    elif request_response['preciptype'] == 'snow':
        weather_image.addIcon(f"{ICON_DIR_PATH}snowflake.png", ICON_SIZE, (LEFT_ALIGNMENT, ITEMS_UP_ALIGNMENT))
        weather_image.drawText(f"{request_response['precipprob']}%", MEDIUM_FONT, (TXT_VERTICAL_ALIGNMENT, ITEMS_UP_ALIGNMENT))
        weather_image.addIcon(f"{ICON_DIR_PATH}snow-depth.png", ICON_SIZE, (CENTRE_ALIGNMENT, ITEMS_UP_ALIGNMENT))
        weather_image.drawText(f"{request_response['snowdepth']}+{request_response['snow']}", MEDIUM_FONT, (TXT_CENTRAL_VERTICAL_ALIGNMENT, ITEMS_UP_ALIGNMENT))
    return weather_image


def _add_wind_data(request_response : dict, weather_image : Image) -> Image:
    """ Add wind information (speed, gust and direction) contained in JSON `request_response`
    to the specified `weather_image`
    ## Parameters:
    * `request_response`: JSON response to the weather request, as a dict
    * `weather_image`: image where add wind data
    ## Return value;
    Weather image with added wind data, for chained calls"""

    #if there is a specified wind speed:
    if request_response['windspeed'] is not None:
        weather_image.addIcon(f"{ICON_DIR_PATH}wind.png", ICON_SIZE, (LEFT_ALIGNMENT, ITEM_HEIGHT + ITEMS_UP_ALIGNMENT))
        weather_image.drawText(f"{request_response['windspeed']}km/h", MEDIUM_FONT, (TXT_VERTICAL_ALIGNMENT, ITEM_HEIGHT + ITEMS_UP_ALIGNMENT))
        weather_image.addIcon(f"{ICON_DIR_PATH}windDirection.png", ICON_SIZE, (LEFT_ALIGNMENT, 2 * ITEM_HEIGHT +  ITEMS_UP_ALIGNMENT), 360 - request_response['winddir'])
        weather_image.drawText(f"{wind_deg2string(request_response['winddir'])}", MEDIUM_FONT, (TXT_VERTICAL_ALIGNMENT, 2 * ITEM_HEIGHT + ITEMS_UP_ALIGNMENT))
    #If there is a specified wind gust
    if request_response['windgust'] is not None:
        weather_image.addIcon(f"{ICON_DIR_PATH}wind.png", ICON_SIZE, (CENTRE_ALIGNMENT, ITEM_HEIGHT + ITEMS_UP_ALIGNMENT), )
        weather_image.drawText(f"{request_response['windgust']}", MEDIUM_FONT, (TXT_CENTRAL_VERTICAL_ALIGNMENT, ITEM_HEIGHT + ITEMS_UP_ALIGNMENT))
    return weather_image


def _add_humidity_data(request_response : dict, weather_image : Image) -> None:
    """ Add humidity information contained in JSON `request_response`
    to the specified `weather_image`
    ## Parameters:
    * `request_response`: JSON response to the weather request, as a dict
    * `weather_image`: image where add humidity data
    ## Return value;
    Weather image with added wind data, for chained calls"""

    weather_image.addIcon(f"{ICON_DIR_PATH}humidity.png", ICON_SIZE, (LEFT_ALIGNMENT, 5 * ITEM_HEIGHT + ITEMS_UP_ALIGNMENT))
    weather_image.drawText(f"{request_response['humidity']}%", MEDIUM_FONT, (TXT_VERTICAL_ALIGNMENT, 5 * ITEM_HEIGHT + ITEMS_UP_ALIGNMENT))


def create_current_weather_image(current_weather : dict, path : str) -> None:
    """Create an image for the API response specified in argument
    ## Parameters :
    * `currentWeather` : response return by the weather API, as a dictionnary
    * `path`: path where save the generated image
    ## Return value :
    An image that represents response from weather API"""

    #Create a basic image according to current weather conditions:
    current_weather_image = _generate_weather_image(current_weather['conditions'])
    #Add temperature data to the image:
    current_weather_image.drawText(f"{round(current_weather['temp'], 1)}°C", BIG_FONT, (LEFT_ALIGNMENT, UP_ALIGNMENT))
    current_weather_image.drawText(f"ressenti {round(current_weather['feelslike'], 1)}°C", MEDIUM_FONT, (LEFT_ALIGNMENT, MIN_MAX_TEMP_ALIGNMENT))
    #Add precipitation data to the image :
    _add_precip_data(current_weather, current_weather_image)
    #Add wind data to the image:
    _add_wind_data(current_weather, current_weather_image)
    #Add atmospheric data to the image:
    current_weather_image.addIcon(f"{ICON_DIR_PATH}pressure.png", ICON_SIZE, (LEFT_ALIGNMENT, 3 * ITEM_HEIGHT + ITEMS_UP_ALIGNMENT))
    current_weather_image.drawText(f"{current_weather['pressure']}hPa", MEDIUM_FONT, (TXT_VERTICAL_ALIGNMENT, 3 * ITEM_HEIGHT + ITEMS_UP_ALIGNMENT))
    current_weather_image.addIcon(f"{ICON_DIR_PATH}visibility.png", ICON_SIZE, (CENTRE_ALIGNMENT, 3 * ITEM_HEIGHT + ITEMS_UP_ALIGNMENT))
    current_weather_image.drawText(f"{int(current_weather['visibility'] * 1000)}m", MEDIUM_FONT, (TXT_CENTRAL_VERTICAL_ALIGNMENT, 3 * ITEM_HEIGHT + ITEMS_UP_ALIGNMENT))
    current_weather_image.addIcon(f"{ICON_DIR_PATH}rays.png", ICON_SIZE, (LEFT_ALIGNMENT, 4 * ITEM_HEIGHT + ITEMS_UP_ALIGNMENT))
    current_weather_image.drawText(f"{current_weather['uvindex']}", MEDIUM_FONT, (TXT_VERTICAL_ALIGNMENT, 4 * ITEM_HEIGHT + ITEMS_UP_ALIGNMENT))
    current_weather_image.addIcon(f"{ICON_DIR_PATH}cloudcover.png", ICON_SIZE, (CENTRE_ALIGNMENT, 4 * ITEM_HEIGHT + ITEMS_UP_ALIGNMENT))
    current_weather_image.drawText(f"{current_weather['cloudcover']}%", MEDIUM_FONT, (TXT_CENTRAL_VERTICAL_ALIGNMENT, 4 * ITEM_HEIGHT + ITEMS_UP_ALIGNMENT))
    #Add humidity data to the image:
    _add_humidity_data(current_weather, current_weather_image)

    current_weather_image.saveImage(path)