#**************************************************#
#              weather  Module File                #
#**************************************************#
#   Authors : Sara MESSARA - Clément PAGES         #
#**************************************************#


BACKGROUNDS_IMAGE_PATH = "./data/images/backgrounds/"
ICON_DIR_PATH = "./data/images/icons/"

DEFAULT_WEATHER_TUPLE = ("Ciel inchangé", f"{BACKGROUNDS_IMAGE_PATH}thinning.png", f"{ICON_DIR_PATH}WeatherIcons/sunAndCloudIcon.png")

dict_weather_type = {
    "type_1" : ("Poudrerie",                    f"{BACKGROUNDS_IMAGE_PATH}snow.png",       f"{ICON_DIR_PATH}WeatherIcons/snowFlackIcon.png"),
    "type_2" : ("bruine",                       f"{BACKGROUNDS_IMAGE_PATH}drizzle.png",    f"{ICON_DIR_PATH}WeatherIcons/mediuùDrizzleIcon.png"),
    "type_3" : ("bruine lourde",                f"{BACKGROUNDS_IMAGE_PATH}drizzle.png",    f"{ICON_DIR_PATH}WeatherIcons/mediumDrizzleIcon.png"),
    "type_4" : ("bruine légère",                f"{BACKGROUNDS_IMAGE_PATH}drizzle.png",    f"{ICON_DIR_PATH}WeatherIcons/lightDrizzleIcon.png"),
    "type_5" : ("forte bruine",                 f"{BACKGROUNDS_IMAGE_PATH}drizzle.png",    f"{ICON_DIR_PATH}WeatherIcons/heavyDrizzleIcon.png"),
    "type_6" : ("légère bruine",                f"{BACKGROUNDS_IMAGE_PATH}drizzle.png",    f"{ICON_DIR_PATH}WeatherIcons/lightDrizzleIcon.png"),
    "type_7" : ("tempête de poussière",         f"{BACKGROUNDS_IMAGE_PATH}dustStorm.png",  f"{ICON_DIR_PATH}WeatherIcons/hurrycaneIcon.png"),
    "type_8" : ("Brouillard",                   f"{BACKGROUNDS_IMAGE_PATH}fog.png",        f"{ICON_DIR_PATH}WeatherIcons/fogIcon.png"),
    "type_9" : ("Bruine verglaçante",           f"{BACKGROUNDS_IMAGE_PATH}blackIce.png",   f"{ICON_DIR_PATH}WeatherIcons/fogIcon.png"),
    "type_10" : ("Forte bruine verglaçante",    f"{BACKGROUNDS_IMAGE_PATH}blackIce.png",   f"{ICON_DIR_PATH}WeatherIcons/snowFlackIcon.png"),
    "type_11" : ("Légère bruine verglaçante",   f"{BACKGROUNDS_IMAGE_PATH}blackIce.png",   f"{ICON_DIR_PATH}WeatherIcons/snowFlackIcon.png"),
    "type_12" : ("Brouillard verglaçant",       f"{BACKGROUNDS_IMAGE_PATH}fog.png",        f"{ICON_DIR_PATH}WeatherIcons/fogIcon.png"),
    "type_13" : ("Forte pluie verglaçante",     f"{BACKGROUNDS_IMAGE_PATH}blackIce.png",   f"{ICON_DIR_PATH}WeatherIcons/heavyRainIcon.png"),
    "type_14" : ("Légère pluie verglaçante",    f"{BACKGROUNDS_IMAGE_PATH}blackIce.png",   f"{ICON_DIR_PATH}WeatherIcons/lightRainIcon.png"),
    "type_15" : ("Tornade",                     f"{BACKGROUNDS_IMAGE_PATH}tornado.png",    f"{ICON_DIR_PATH}WeatherIcons/hurrycaneIcon.png"),
    "type_16" : ("Chute de grêle",              f"{BACKGROUNDS_IMAGE_PATH}storm.png",      f"{ICON_DIR_PATH}WeatherIcons/stormIcon.png"),
    "type_17" : ("Grezzil",                     f"{BACKGROUNDS_IMAGE_PATH}snow.png",       f"{ICON_DIR_PATH}WeatherIcons/stormIcon.png"),
    "type_18" : ("foudre sans tonnerre",        f"{BACKGROUNDS_IMAGE_PATH}storm.png",      f"{ICON_DIR_PATH}WeatherIcons/stormIcon.png"),
    "type_19" : ("Brume",                       f"{BACKGROUNDS_IMAGE_PATH}fog.png",        f"{ICON_DIR_PATH}WeatherIcons/fogIcon.png"),
    "type_20" : ("Précipations à proximité",    f"{BACKGROUNDS_IMAGE_PATH}rain.png",       f"{ICON_DIR_PATH}WeatherIcons/mediumRainIcon.png"),
    "type_21" : ("Pluie",                       f"{BACKGROUNDS_IMAGE_PATH}rain.png",       f"{ICON_DIR_PATH}WeatherIcons/mediumRainIcon.png"),
    "type_22" : ("Forte pluie et neige",        f"{BACKGROUNDS_IMAGE_PATH}snow.png",       f"{ICON_DIR_PATH}WeatherIcons/heavyRainIcon.png"),
    "type_23" : ("Légère pluie et neige",       f"{BACKGROUNDS_IMAGE_PATH}snow.png",       f"{ICON_DIR_PATH}WeatherIcons/lightRainIcon.png"),
    "type_24" : ("Averse",                      f"{BACKGROUNDS_IMAGE_PATH}rain.png",       f"{ICON_DIR_PATH}WeatherIcons/heavyRainIcon.png"),
    "type_25" : ("Forte pluie",                 f"{BACKGROUNDS_IMAGE_PATH}rain.png",       f"{ICON_DIR_PATH}WeatherIcons/heavyRainIcon.png"),
    "type_26" : ("Légère pluie",                f"{BACKGROUNDS_IMAGE_PATH}rain.png",       f"{ICON_DIR_PATH}WeatherIcons/lightRainIcon.png"),
    "type_27" : ("Eclaircissement",             f"{BACKGROUNDS_IMAGE_PATH}thinning.png",   f"{ICON_DIR_PATH}WeatherIcons/sunAndCloudIcon.png"),
    "type_28" : ("Assombrissement",             f"{BACKGROUNDS_IMAGE_PATH}cloudy.png",     f"{ICON_DIR_PATH}WeatherIcons/cloudyIcon.png"),
    "type_29" : ("Ciel inchangé",               f"{BACKGROUNDS_IMAGE_PATH}thinning.png",   f"{ICON_DIR_PATH}WeatherIcons/sunAndCloudIcon.png"),
    "type_30" : ("Fumée",                       f"{BACKGROUNDS_IMAGE_PATH}smoke.png",      f"{ICON_DIR_PATH}WeatherIcons/fogIcon.png"),
    "type_31" : ("Neige",                       f"{BACKGROUNDS_IMAGE_PATH}snow.png",       f"{ICON_DIR_PATH}WeatherIcons/mediumSnowFallIcon.png"),
    "type_32" : ("Pluie et neige mêlée",        f"{BACKGROUNDS_IMAGE_PATH}snow.png",       f"{ICON_DIR_PATH}WeatherIcons/mediumSnowFallIcon.png"),
    "type_33" : ("Chutes de neige",             f"{BACKGROUNDS_IMAGE_PATH}snow.png",       f"{ICON_DIR_PATH}WeatherIcons/heavySnowFallIcon.png"),
    "type_34" : ("Averses de neige",            f"{BACKGROUNDS_IMAGE_PATH}snow.png",       f"{ICON_DIR_PATH}WeatherIcons/heavySnowFallIcon.png"),
    "type_35" : ("Quelques flocons",            f"{BACKGROUNDS_IMAGE_PATH}snow.png",       f"{ICON_DIR_PATH}WeatherIcons/lightSnowFallIcon.png"),
    "type_36" : ("Grains",                      f"{BACKGROUNDS_IMAGE_PATH}snow.png",       f"{ICON_DIR_PATH}WeatherIcons/lightSnowFallIcon.png"),
    "type_37" : ("Orage",                       f"{BACKGROUNDS_IMAGE_PATH}storm.png",      f"{ICON_DIR_PATH}WeatherIcons/stormIcon.png"),
    "type_38" : ("Orage sans précipitation",    f"{BACKGROUNDS_IMAGE_PATH}storm.png",      f"{ICON_DIR_PATH}WeatherIcons/stormIcon.png"),
    "type_39" : ("Voilé",                       f"{BACKGROUNDS_IMAGE_PATH}cloudyHaze.png", f"{ICON_DIR_PATH}WeatherIcons/hazeIcon.png"),
    "type_40" : ("Blizzard",                    f"{BACKGROUNDS_IMAGE_PATH}snow.png",       f"{ICON_DIR_PATH}WeatherIcons/hurrycaneIcon.png"),
    "type_41" : ("Couvert",                     f"{BACKGROUNDS_IMAGE_PATH}cloudy.png",     f"{ICON_DIR_PATH}WeatherIcons/cloudyIcon.png"),
    "type_42" : ("Partiellement nuageux",       f"{BACKGROUNDS_IMAGE_PATH}thinning.png",   f"{ICON_DIR_PATH}WeatherIcons/sunAndCloudIcon.png"),
    "type_43" : ("Ensoleillé",                  f"{BACKGROUNDS_IMAGE_PATH}sun.png",        f"{ICON_DIR_PATH}WeatherIcons/sunIcon.png"),
}


def get_path_image_weather_type(weather_condition : str) -> str :
    """Get path to the image corresponding to weather conditions type specified in argument
    ## Parameters:
    * `weatherCondition`: weather condition returned by the API, as a string
    ## Return value:
    path to the image as a string"""

    first_type = weather_condition.split(",")[0]
    return dict_weather_type.get(first_type, DEFAULT_WEATHER_TUPLE)[1]


def get_description_weather_type(weather_condition : str) -> str :
    """Get weather description of the weather condition type specified in argument
    ## Parameters: 
    * `weatherCondition`: weather condition returned by the API, as a string
    ### Return value:
    weather description as string
    """

    first_type = weather_condition.split(",")[0]
    return dict_weather_type.get(first_type, DEFAULT_WEATHER_TUPLE)[0]


def get_icon_path_weather_type(weather_condition : str) -> str :
    """Get weather icon path corresponding to weather condition type specified in argument
    ## Parameters: 
    * `weatherCondition`: weather condition returned by the API, as a string
    ## Return value:
    weather icon path as string"""

    first_type = weather_condition.split(",")[0]
    return dict_weather_type.get(first_type, DEFAULT_WEATHER_TUPLE)[2]


def wind_deg2string(wind_direction: int) -> str:
    """Gives the wind direction as a cardinal direction from the angle specified
    in argument
    ## Parameters:
    * `wind_direction`: direction of the wind in degree, starting from the north
    ## Return value:
    Wind cardinal direction, as a string"""

    if wind_direction < 157:
        if wind_direction < 67:
            if wind_direction < 22:
                return "N"
            return "NE"
        if wind_direction < 112:
            return "E"
        return "SE"
    if wind_direction < 257:
        if wind_direction < 212:
            return "S"
        return "SW"
    if wind_direction < 292:
        return "W"
    return "NW"