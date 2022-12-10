#Importation des différents modules
import os
import discord
from discord.ext import commands
from discord import app_commands
import threading
import json
import requests
import numpy as np
import time
from PIL import Image
import logging

from BotController import BotController


#=======================
#    GLOBAL VARIABLES
#=======================

#Declare a bot instance :
phyxit = commands.Bot(command_prefix='+', intents=discord.Intents.all())
controller = BotController(phyxit)
#Declare a logger for debugging purposes:
logging.basicConfig(level=logging.INFO)




#==================================
#        BOT EVENTS
#==================================


@phyxit.event
async def on_ready():
  await controller.on_ready()


@phyxit.event
async def on_message(message):
  await controller.on_message(message)


#====================
#    BOT'S COMMANDS
#====================


@phyxit.tree.command(name="ping", description="Si je suis réveillé, je réponds pong! Sinon... et bien c'est que je dors 😴", guild=discord.Object(id=1049605745995415574))
async def ping(interaction : discord.Interaction):
  await controller.ping(interaction)


@phyxit.tree.command(name="ajoute_ville", description="Ajoute une ville pour laquelle vous souhaitez obtenir la météo, dans la limite de 6 villes", guild=discord.Object(id=1049605745995415574))
@app_commands.describe(nom_localite="Nom de la ville")
async def ajouterVille(interaction : discord.Interaction, nom_localite : str):
  await controller.addCity(interaction, nom_localite)


#####################################################################################################
#ALWAYS RUN PART - DO NOT PUT ANYTHING BELOW - ALWAYS RUN PART - DO NOT PUT ANYTHING BELOW 
#####################################################################################################

phyxit.run("MTA0OTYxMTk0OTUyMjAyNjUxNg.GAjQUa.w4UbRBs1zb7uGlPUkFU0XLp0FxxjL1icaSSvxQ")