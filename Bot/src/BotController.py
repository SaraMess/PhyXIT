
import discord
from discord.ext import commands
import logging

from VisualCrossingHandler import VisualCrossingHandler

class BotController:

    def __init__(self, discordBot : commands.Bot) -> None :
        """"""
        self.bot = discordBot
        self.vc_handler = VisualCrossingHandler()
    

    async def on_ready(self) -> None:
        """"""
        logging.info("Synchronize bot command tree to discord")
        await self.bot.tree.sync(guild=discord.Object(id=1049605745995415574))
        logging.info("Starting Visual Crossing Handler")
        self.vc_handler.start()
        logging.info("Bot is ready to use!")


    async def on_message(self, message) -> None:
        """"""
        logging.info("A message was received")
        await self.bot.process_commands(message)
    

    async def ping(self, interaction : discord.Interaction) -> None:
        """"""
        await interaction.response.send_message("Pong !")

    
    async def addCity(self, interaction : discord.Interaction, location_name) -> None:
        """"""
        
        res = self.vc_handler.add_city(location_name)
        if res == -1:
            await interaction.response.send_message("Le nombre de ville maximum autorisé (6) a été atteint")
        elif res == -2:
            await interaction.response.send_message(f"La localisation {location_name} ne semble pas exister dans les données de Visual Crossing")
        else:
            await interaction.response.send_message(f"La localisation {location_name} a été ajoutée avec succès!")
