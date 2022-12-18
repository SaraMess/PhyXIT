#**************************************************#
#          Bot Controller Class File               #
#**************************************************#
#   Authors : Sara MESSARA - Clément PAGES         #
#**************************************************#


#========================================#
#       Modules used in this file        #
#========================================#

import asyncio
import discord
from discord.ext import commands
import logging
import time

import VisualCrossingHandler as vc_handler
from weatherImager import create_current_weather_image


FREQ_MINUTES = 1

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
        self.cities_data = {"Toulouse" : [], "Alger" : []}
        self.weather_last_msg_ref = {"Toulouse" : (-1, None), "Alger" : (-1, None)}
        #Mutex:
        self._lock_cities_data = asyncio.Lock()
        self._lock_msg_ref = asyncio.Lock()


    async def on_ready(self) -> None:
        """Method called when the bot is ready to work
        ## Return value:
        Not applicable"""

        logging.info("Synchronize bot command tree to discord")
        await self.bot.tree.sync(guild=discord.Object(id=1049605745995415574))
        logging.info("Starting acquiring weather data from Visual Crossing API")
        loop = asyncio.get_event_loop()
        loop.create_task(self._get_weather())
        logging.info("Bot is ready to use!")


    def get_city_list(self) -> list:
        """Returns a list containing all the cities for which the bot requests the
        weather to the API
        ## Return value:
        A list of city names"""
    
        return self.cities_data.keys()


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
        await self._lock_cities_data.acquire()
        if len(self.cities_data) == 6:
            self._lock_cities_data.release()
            logging.error("Limit for number of cities has been reached")
            await interaction.response.send_message("Le nombre de ville maximum autorisé (6) a été atteint")
            return
        #Test if the specified location exists on VisualCrossing by performing a request
        #for this location:
        if self.vc_handler.currentWeatherRequest(location_name) == {}:
            self._lock_cities_data.release()
            logging.error(f"An error occured while performing a request for {location_name}. \
            It seems that this city is not known by Visual Crossing API")
            await interaction.response.send_message(f"La localisation {location_name} ne semble pas exister dans les données de Visual Crossing")
            return
        self.cities_data[location_name] = []
        self._lock_cities_data.release()
        await self._lock_msg_ref.acquire()
        self.weather_last_msg_ref[location_name] = (-1, None)
        self._lock_msg_ref.release()
        await interaction.response.send_message(f"La localisation {location_name} a été ajoutée avec succès!")


    async def delete_city(self, interaction : discord.Interaction, location_name : str) -> None:
        """"""

        if location_name not in self.get_city_list():
            await interaction.response.send_message(f"La localisation {location_name} n'existe pas dans mes données :/")
        else:
            del self.cities_data[location_name]
            del self.weather_last_msg_ref[location_name]
            await interaction.response.send_message(f"La localisation {location_name} a bien été supprimée !")

    
    async def send_weather(self, interacion : discord.Interaction, location_name : str):
        """"""

        #Firsly, tests if the city is known by the bot:
        if location_name not in self.get_city_list():
            await interacion.response.send_message(f"Navré, mais je n'ai pas d'information sur la météo à {location_name}. Essayez tout d'abord de l'ajouter !")
        else:
            #If command was already called for the current location and not stopped, delete the last message sent
            #for the specified lodation and generate a new one:
            await self._lock_msg_ref.acquire()
            last_msg_id = self.weather_last_msg_ref[location_name][0]
            self._lock_msg_ref.release()
            if last_msg_id != -1:
                msg_to_delete = await interacion.channel.fetch_message(last_msg_id)
                try:
                    await msg_to_delete.delete()
                except discord.NotFound:
                    logging.warning(f"Message {last_msg_id} was already deleted. Nothing to do.")
                except discord.HTTPException:
                    logging.error(f"message {last_msg_id} cannot be deleted.")
                    return
            #Send generated image in a new message and save the id of this message:
            create_current_weather_image(self.cities_data[location_name][-1], f"./data/{location_name}_current_weather.png")
            try:
                await interacion.response.send_message(f"Voici la météo actuelle à {location_name}", file=discord.File(f"./data/{location_name}_current_weather.png"))
            except discord.HTTPException:
                logging.error("Message in response to weather command was not sent")
                return
            #Get the id of the last message, which corresponds to the weather image sent:
            id_msg = interacion.channel.last_message_id
            await self._lock_msg_ref.acquire()
            self.weather_last_msg_ref[location_name] = (id_msg, interacion.channel)
            self._lock_msg_ref.release()


    async def stop_weather(self, interaction : discord.Interaction, location_name : str) -> None:
        """"""

        await self._lock_msg_ref.acquire()
        last_msg_id = self.weather_last_msg_ref.get(location_name, (-2, None))[0]
        self._lock_msg_ref.release()
        #If specified location is unknown for the bot:
        if last_msg_id == -2:
            logging.info(f"stop_weather command: {location_name} is unknown")
            await interaction.response.send_message(f"Hmmm... La localité {location_name} n'est pas dans mes données!")
        #If weather command was not called for the specified location:
        elif last_msg_id == -1:
            logging.info(f"weather for location {location_name} is not currently sent by the bot. Nothing to do")
            await interaction.response.send_message(f"Je n'envoie actuellement pas la météo pour la localité {location_name}")
        #Else, stop sending weather data for the specified location:
        else:
            await self._lock_msg_ref.acquire()
            self.weather_last_msg_ref[location_name] = (-1, None)
            self._lock_msg_ref.release()
            await interaction.response.send_message(f"Bien compris, je n'enverrai plus la météo pour la localité {location_name}")


    async def _get_weather(self) -> None:
        """This async task method corresponds to the management of the weather requests 
        for the cities specified by the user. This task also transmits the 
        data to the discord interface in case the user has requested it"""

        #Run forever
        while True:
            #Get weather every FREQ_MINUTES minutes
            await asyncio.sleep(60 * FREQ_MINUTES)
            current_time = time.localtime()
            logging.info(f"{current_time[3]}:{current_time[4]} ==> Getting weather data...")
            #Get weather data for each specified city:
            await self._lock_cities_data.acquire()
            for location_name in self.cities_data:
                logging.info(f"Getting weather for {location_name}")
                current_data = vc_handler.currentWeatherRequest(location_name)
                logging.info(f"data strucutre received : {current_data}")
                #If there are less than 6 hours of data:
                if len(self.cities_data[location_name]) < 6 * (60 / FREQ_MINUTES):
                    self.cities_data[location_name].append(current_data)
                #Else remove the first sample, to keep 6 hours of data:
                else:
                    self.cities_data[location_name] = self.cities_data[location_name][1:].append(current_data)
                await self._lock_msg_ref.acquire()
                last_msg_id = self.weather_last_msg_ref[location_name][0]
                channel : discord.TextChannel = self.weather_last_msg_ref[location_name][1]
                self._lock_msg_ref.release()
                #If command "meteo" was called by the user for the current city and not stopped:
                if last_msg_id != -1:
                    create_current_weather_image(current_data, f"./data/{location_name}_current_weather.png")
                    msg_to_del = await channel.fetch_message(last_msg_id)
                    #Try to delete previous webhook message:
                    try:
                        await msg_to_del.delete()
                    except discord.NotFound:
                        logging.warning(f"Message {last_msg_id} was already deleted. Nothing to do.")
                    except discord.HTTPException:
                        logging.error("Message in response to weather command was not sent")
                    else:
                        #try to send new webhook message:
                        try:
                            await channel.send(content=f"Voici la météo actuelle à {location_name}", file=discord.File(f"./data/{location_name}_current_weather.png"))
                            #self.default_webhook.send(content=f"Voici la météo actuelle à {city_name}", file=discord.File(f"./data/{city_name}_current_weather.png"))
                        except discord.NotFound:
                            logging.error("Webhook used to send weather data was not found.")
                        except discord.HTTPException:
                            logging.error("Webhook was not sent")
                        else:
                            await self._lock_msg_ref.acquire()
                            self.weather_last_msg_ref[location_name] = (channel.last_message_id, channel)
                            self._lock_msg_ref.release()
            self._lock_cities_data.release()