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

from VisualCrossingHandler import VisualCrossingHandler



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


    async def on_ready(self) -> None:
        """Method called when the bot is ready to work
        ## Return value:
        Not applicable"""

        logging.info("Synchronize bot command tree to discord")
        await self.bot.tree.sync(guild=discord.Object(id=1049605745995415574))
        logging.info("Starting Visual Crossing Handler")
        self.vc_handler.start()
        logging.info("Bot is ready to use!")


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


    async def addCity(self, interaction : discord.Interaction, location_name : str) -> None:
        """Add the specified location to the list of cities for which the bot 
        should search the weather.
        ## Parameters:
        * `ìnteraction`: reference to the interaction that generated the call to the command
        * `location_name`: name of the location to add
        ## Return value :
        not applicable"""
        
        res = self.vc_handler.add_city(location_name)
        if res == -1:
            await interaction.response.send_message("Le nombre de ville maximum autorisé (6) a été atteint")
        elif res == -2:
            await interaction.response.send_message(f"La localisation {location_name} ne semble pas exister dans les données de Visual Crossing")
        else:
            await interaction.response.send_message(f"La localisation {location_name} a été ajoutée avec succès!")


    async def delete_city(self, interaction : discord.Interaction, location_name : str) -> None:
        """"""

        if location_name not in self.vc_handler.get_city_list():
            await interaction.response.send_message(f"La localisation {location_name} n'existe pas dans mes données :/")
        else:
            await interaction.response.send_message(f"La localisation {location_name} a bien été supprimée !")