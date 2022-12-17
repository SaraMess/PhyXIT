#**************************************************#
#          Bot Controller Class File               #
#**************************************************#
#   Authors : Sara MESSARA - Clément PAGES         #
#**************************************************#


#========================================#
#       Modules used in this file        #
#========================================#

import discord
from discord.ext import commands
import logging
import threading
import time

from VisualCrossingHandler import VisualCrossingHandler
from weatherImager import create_current_weather_image


FREQ_MINUTES = 10

#===============================#
#       Class Declaration       #
#===============================#

class BotController:

    def __init__(self, discord_bot : commands.Bot) -> None :
        """Class constructor.
        ## Parameters:
        * `discord_bot`: reference to the discord bot object
        ## Return value:
        Not applicable"""

        self.bot = discord_bot
        self.vc_handler = VisualCrossingHandler()
        self.citiesData = {"Toulouse" : [], "Alger" : []}

        self.get_weather_thread = threading.Thread(target=self._get_weather)


    async def on_ready(self) -> None:
        """Method called when the bot is ready to work
        ## Return value:
        Not applicable"""

        logging.info("Synchronize bot command tree to discord")
        await self.bot.tree.sync(guild=discord.Object(id=1049605745995415574))
        logging.info("Starting acquiring weather data from Visual Crossing API")
        self.get_weather_thread.start()
        logging.info("Bot is ready to use!")


    def get_city_list(self) -> list:
        """Returns a list containing all the cities for which the bot requests the
        weather to the API
        ## Return value:
        A list of city names"""

        return self.citiesData.keys()


    async def on_message(self, message) -> None:
        """Method called when a message is sent on a server where the bot belongs
        ## Parameters:
        * `message`: reference to the message object that triggers the event
        ## Return value:
        Not applicable"""

        logging.info("A message was received")
        await self.bot.process_commands(message)
    

    async def ping(self, interaction : discord.Interaction) -> None:
        """This method allows to test if the bot is alive or not.
        ## Parameters:
        * `ìnteraction`: reference to the interaction that generated the call to the command
        ## Return value:
        Not applicable"""

        await interaction.response.send_message("Pong !")


    async def add_city(self, interaction : discord.Interaction, location_name : str) -> None:
        """Add the specified location to the list of cities for which the bot 
        should search the weather.
        ## Parameters:
        * `ìnteraction`: reference to the interaction that generated the call to the command
        * `location_name`: name of the location to add
        ## Return value :
        not applicable"""

        #Test if it is possible to add one more city:
        if len(self.citiesData) == 6:
            logging.error("Limit for number of cities has been reached")
            await interaction.response.send_message("Le nombre de ville maximum autorisé (6) a été atteint")
            return
        #Test if the specified location exists on VisualCrossing by performing a request
        #for this location:
        if self.vc_handler.currentWeatherRequest(location_name) == {}:
            logging.error(f"An error occured while performing a request for {location_name}. \
            It seems that this city is not known by Visual Crossing API")
            await interaction.response.send_message(f"La localisation {location_name} ne semble pas exister dans les données de Visual Crossing")
            return
        self.citiesData[location_name] = []
        await interaction.response.send_message(f"La localisation {location_name} a été ajoutée avec succès!")


    async def delete_city(self, interaction : discord.Interaction, location_name : str) -> None:
        """"""

        if location_name not in self.get_city_list():
            await interaction.response.send_message(f"La localisation {location_name} n'existe pas dans mes données :/")
        else:
            del self.citiesData[location_name]
            await interaction.response.send_message(f"La localisation {location_name} a bien été supprimée !")
    

    def _get_weather(self) -> None:
        """This method corresponds to the thread managing the weather requests 
        for the cities specified by the user. This thread also transmits the 
        data to the discord interface in case the user has requested it"""

        #Run forever
        while True:
            #Get weather every 10 minutes
            time.sleep(60 * FREQ_MINUTES)
            current_time = time.localtime()
            logging.info(f"{current_time[3]}:{current_time[4]} ==> Getting weather data...")
            #Get weather data for each specified city:
            for city in self.citiesData:
                logging.info(f"Getting weather for {city}")
                current_data = self.vc_handler.currentWeatherRequest(city)
                logging.info(f"data strucutre received : {current_data}")
                #If there are less than 6 hours of data:
                if len(self.citiesData[city]) < 6 * (60 / FREQ_MINUTES):
                    self.citiesData[city].append(current_data)
                #Else remove the first sample, to keep 6 hours of data:
                else:
                    self.citiesData[city] = self.citiesData[city][1:].append(current_data)