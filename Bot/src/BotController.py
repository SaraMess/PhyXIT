#**************************************************#
#          Bot Controller Class File               #
#**************************************************#
#   Authors : Sara MESSARA - Clément PAGES         #
#**************************************************#


#========================================#
#       Modules used in this file        #
#========================================#

import asyncio
import asyncio
from dis import disco
import discord
from discord.ext import commands
import logging
import numpy as np
import time

import graphic
import VisualCrossingHandler as vc_handler
from weatherImager import create_current_weather_image
import paho.mqtt.client as mqtt


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
        self.cities_data = {"Toulouse" : [], "Alger" : []}
        self.weather_last_msg_ref = {"Toulouse" : (-1, None), "Alger" : (-1, None)}
        #Mutex:
        self._lock_cities_data = asyncio.Lock()
        self._lock_msg_ref = asyncio.Lock()

        self.mqtt_message = ""
        self.mqtt_data = {"temp" : [], "humi" : [], "rang" : []}


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


    async def get_city_list(self) -> list:
        """Returns a list containing all the cities for which the bot requests the
        weather to the API
        ## Return value:
        A list of cities represented by their name
        """
        await self._lock_cities_data.acquire()
        city_list = list(self.cities_data.keys())
        self._lock_cities_data.release()
        return city_list
    

    def get_available_data_type(self) -> list:
        """"""

        return list(self.mqtt_data.keys())
    

    async def get_enabled_cities_list(self) -> list:
        """Returns a list with the location for which the bot currently send the
        weather on discord.
        ## Return value :
        A list of cities represented by their name
        """
        
        location_list = []
        await self._lock_msg_ref.acquire()
        for location_name in self.weather_last_msg_ref.keys():
            if self.weather_last_msg_ref[location_name][0] != -1:
                location_list.append(location_name)
        self._lock_msg_ref.release()
        return location_list


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
        if len(await self.get_city_list()) == 6:
            logging.error("Limit for number of cities has been reached")
            await interaction.response.send_message("Le nombre maximal de villes autorisé (6) a été atteint, supprimez une ville puis réessayez!")
            return
        #If location is already known by the bot, do nothing:
        if location_name in await self.get_city_list():
            await interaction.response.send_message(f"La localisation {location_name} a déjà été ajoutée. Vous pouvez utiliser la commande /meteo.")
            return
        #Test if the specified location exists on VisualCrossing by performing a request
        #for this location:
        current_data = vc_handler.currentWeatherRequest(location_name)
        if current_data == {}:
            logging.error(f"An error occured while performing a request for {location_name}. It seems that this city is not known by Visual Crossing API")
            await interaction.response.send_message(f"La localisation {location_name} ne semble pas exister dans les données de Visual Crossing")
        else:
            #Create data list for the current location and add the first acquired data:
            await self._add_location(location_name)
            await self._add_data_to_location(location_name, current_data)
            create_current_weather_image(current_data, f"./data/{location_name}_current_weather.png")
            await interaction.response.send_message(f"La localisation {location_name} a été ajoutée avec succès!")


    async def get_esp32_data(self, interaction : discord.Interaction, data_type : str) -> None:
        #If specified data type is "all":
        if data_type == "all":
            graphic.generate_all_graph(self.mqtt_data)
            await interaction.response.send_message("Voici l'ensemble des statistiques en provenance de l'esp32", file=discord.File(f"{graphic.GRAPHIC_SAVE_PATH}all_graph.png"))
        #If specified data is known:
        elif data_type in self.mqtt_data.keys():
            graphic.generate_unique_graph(self.mqtt_data[data_type], data_type)
            await interaction.response.send_message(f"Voici le graphe correspondant pour {data_type}", file=discord.File(f"{graphic.GRAPHIC_SAVE_PATH}{data_type}_graph.png"))

        else:
            await interaction.response.send_message("Je ne reconnais pas le type de données indiqué !")


    async def delete_city(self, interaction : discord.Interaction, location_name : str) -> None:
        """"""

        if location_name not in await self.get_city_list():
            await interaction.response.send_message(f"La localisation {location_name} n'existe pas dans mes données :/")
        else:
            await self._delete_location(location_name)
            await interaction.response.send_message(f"La localisation {location_name} a bien été supprimée !")

    
    async def send_weather(self, interacion : discord.Interaction, location_name : str):
        """"""

        #Firsly, tests if the city is known by the bot:
        if location_name not in await self.get_city_list():
            await interacion.response.send_message(f"Navré, mais je n'ai pas d'information sur la météo à {location_name}. Essayez tout d'abord de l'ajouter !")
        else:
            #If command was already called for the current location and not stopped, delete the last message sent
            #for the specified lodation and generate a new one:
            last_msg_id = (await self._get_location_last_msg_info(location_name))[0]
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
            create_current_weather_image((await self._get_location_data(location_name))[-1], f"./data/{location_name}_current_weather.png")
            try:
                await interacion.response.send_message(f"Voici la météo actuelle à {location_name}", file=discord.File(f"./data/{location_name}_current_weather.png"))
            except discord.HTTPException:
                logging.error("Message in response to weather command was not sent")
                return
            #Get the id of the last message, which corresponds to the weather image sent:
            id_msg = interacion.channel.last_message_id
            await self._set_location_last_msg_info(location_name, id_msg, interacion.channel)


    async def stop_weather(self, interaction : discord.Interaction, location_name : str) -> None:
        """"""

        last_msg_id = (await self._get_location_last_msg_info(location_name))[0]
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
            await self._set_location_last_msg_info(location_name, -1, None)
            await interaction.response.send_message(f"Bien compris, je n'enverrai plus la météo pour la localité {location_name}")


    async def get_cities_status(self, interaction : discord.Interaction) -> None :
        """Build and send an embed message with status data about added cities.
        This embed indicates for which known cities the user currently get the
        weather.
        ## Parameters:
        * `ìnteraction`: reference to the interaction that generated the call to the command
        ## Return value:
        Not applicable
        """

        embed_status = discord.Embed(title="Voici les villes connues par PhyXIT", description= f"Nombre de villes ajoutées {len(self.weather_last_msg_ref)}/6", color=0x87CEEB)
        #Get status for all added cities:
        for city_name in await self.get_city_list():
            if (await self._get_location_last_msg_info(city_name))[0] == -1:
                embed_status.add_field(name=city_name, value="météo actuellement non transmise", inline=False)
            else:
                embed_status.add_field(name=city_name, value="transmission de la météo activée", inline=False)
        try:
            await interaction.response.send_message(content="", embed=embed_status)
        except discord.HTTPException as e:
            logging.error(f"Status embed was not sent. Reason : {e.text}")


    async def _add_location(self, location_name : str) -> None:
        """"""

        await self._lock_cities_data.acquire()
        self.cities_data[location_name] = []
        self._lock_cities_data.release()
        await self._lock_msg_ref.acquire()
        self.weather_last_msg_ref[location_name] = (-1, None)
        self._lock_msg_ref.release()


    async def _delete_location(self, location_name : str) -> None:
        """"""

        await self._lock_cities_data.acquire()
        await self._lock_msg_ref.acquire()
        try:
            del self.cities_data[location_name]
            del self.weather_last_msg_ref[location_name]
        except KeyError:
            logging.warning(f"Warning in {self._delete_location.__name__}: location {location_name} is not known. Do nothing")
        self._lock_msg_ref.release()
        self._lock_cities_data.release()


    async def _add_data_to_location(self, location_name : str, data : dict) -> None:
        """"""

        await self._lock_cities_data.acquire()
        try:
            #If there are more than 6 hours of data, delete the most older data:
            if len(self.cities_data[location_name]) >= 6 * (60 / FREQ_MINUTES):
                self.cities_data[location_name] = self.cities_data[location_name][1:]
            self.cities_data[location_name].append(data)
        except KeyError:
            logging.error(f"Error in {self._add_data_to_location.__name__}: trying to add data to unknown city {location_name}. Abort")
        self._lock_cities_data.release()


    async def _get_location_data(self, location_name) -> None:
        """"""

        await self._lock_cities_data.acquire()
        try:
            data = self.cities_data[location_name]
        except KeyError:
            logging.error(f"Error in {self._get_location_data.__name__}: trying to retrieve data for an unknown city {location_name}. Abort")
            return
        except IndexError:
            logging.error(f"Error in {self._get_location_data.__name__}: No data available for location {location_name}")
            return
        finally:
            self._lock_cities_data.release()
        return data


    async def _get_location_last_msg_info(self, location_name : str) -> tuple:
        """"""

        await self._lock_msg_ref.acquire()
        try:
            msg_info = self.weather_last_msg_ref[location_name]
        except KeyError:
            logging.error(f"Error in {self._get_location_last_msg_info.__name__}: location {location_name} is unknow. Abort")
            return (-2, None)
        finally:
            self._lock_msg_ref.release()
        return msg_info


    async def _set_location_last_msg_info(self, location_name : str, last_msg_id : int, last_channel) -> None:
        """"""

        await self._lock_msg_ref.acquire()
        if location_name not in await self.get_city_list():
            logging.error(f"Error in {self._set_location_last_msg_info.__name}: location {location_name} is unknown. Do nothing")
        else:
            self.weather_last_msg_ref[location_name] = (last_msg_id, last_channel)
        self._lock_msg_ref.release()


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
            cities_list = await self.get_city_list()
            for location_name in cities_list:
                logging.info(f"Getting weather for {location_name}")
                current_data = vc_handler.currentWeatherRequest(location_name)
                logging.info(f"data strucutre received : {current_data}")
                await self._add_data_to_location(location_name, current_data)
                last_msg_id, channel = await self._get_location_last_msg_info(location_name)
                #If command "meteo" was called by the user for the current city and not stopped:
                if last_msg_id != -1:
                    create_current_weather_image(current_data, f"./data/{location_name}_current_weather.png")
                    #Try to delete previous webhook message:
                    try:
                        msg_to_del = await channel.fetch_message(last_msg_id)
                        await msg_to_del.delete()
                    except discord.NotFound:
                        logging.warning(f"Message {last_msg_id} was already deleted. Nothing to do.")
                    except discord.HTTPException:
                        logging.error("Message in response to weather command was not deleted")
                    #try to send new webhook message:
                    try:
                        await channel.send(content=f"Voici la météo actuelle à {location_name}", file=discord.File(f"./data/{location_name}_current_weather.png"))
                        #self.default_webhook.send(content=f"Voici la météo actuelle à {city_name}", file=discord.File(f"./data/{city_name}_current_weather.png"))
                    except discord.NotFound:
                        logging.error("Webhook used to send weather data was not found.")
                    except discord.HTTPException:
                        logging.error("Webhook was not sent")
                    else:
                        await self._set_location_last_msg_info(location_name, channel.last_message_id, channel)
