#**************************************************#
#                 main.pyFile                      #
#**************************************************#
#   Authors : Sara MESSARA - Clément PAGES         #
#**************************************************#


#========================================#
#       Modules used in this file        #
#========================================#

import discord
from discord.ext import commands
from discord import app_commands
import logging
import os
import typing

from BotController import BotController



#===================================#
#   Global Variables Declarations   # 
#===================================#

#Declare a bot instance :
phyxit = commands.Bot(command_prefix='+', intents=discord.Intents.all())
controller = BotController(phyxit)
#Declare a logger for debugging purposes:
logging.basicConfig(level=logging.INFO)



#==============================#
#   Bot Events Declarations    #
#==============================#

@phyxit.event
async def on_ready():
  await controller.on_ready()


@phyxit.event
async def on_message(message):
  await controller.on_message(message)



#====================
#    BOT'S COMMANDS
#====================

async def available_cities_autocomplete(interaction : discord.Interaction, current : str) -> typing.List[app_commands.Choice[str]]:
  choices_list = []
  for city_choice in controller.get_city_list():
    if current.lower() in city_choice.lower():
      choices_list.append(app_commands.Choice(name=city_choice, value=city_choice))
  return choices_list


async def enabled_cities_autocomplete(interaction : discord.Interaction, current : str) -> typing.List[app_commands.Choice[str]]:
  choices_list = []
  for city_choice in controller.get_enabled_cities_list():
    if current.lower() in city_choice.lower():
      choices_list.append(app_commands.Choice(name=city_choice, value=city_choice))
  return choices_list


@phyxit.tree.command(name="ping", description="Si je suis réveillé, je réponds pong! Sinon... et bien c'est que je dors 😴", guild=discord.Object(id=1049605745995415574))
async def ping(interaction : discord.Interaction):
  await controller.ping(interaction)


@phyxit.tree.command(name="ajoute_ville", description="Ajoute une ville pour laquelle vous souhaitez obtenir la météo, dans la limite de 6 villes", guild=discord.Object(id=1049605745995415574))
@app_commands.describe(nom_localite="Nom de la ville à ajouter")
async def ajouterVille(interaction : discord.Interaction, nom_localite : str):
  await controller.add_city(interaction, nom_localite)


@phyxit.tree.command(name="suppr_ville", description="Supprime une ville de la liste des villes ajoutées", guild=discord.Object(id=1049605745995415574))
@app_commands.describe(nom_localite="Nom de la ville à supprimer")
@app_commands.autocomplete(nom_localite=available_cities_autocomplete)
async def delete_city(interaction : discord.Interaction, nom_localite : str):
  await controller.delete_city(interaction, nom_localite)


@phyxit.tree.command(name="meteo", description="Donne la météo pour la ville indiquée", guild=discord.Object(id=1049605745995415574))
@app_commands.describe(nom_localite="Nom de la ville")
@app_commands.autocomplete(nom_localite=available_cities_autocomplete)
async def get_weather(interaction : discord.Interaction, nom_localite : str):
  await controller.send_weather(interaction, nom_localite)


@phyxit.tree.command(name="stop", description="Stoppe l'envoi de la météo pour la ville indiquée", guild=discord.Object(id=1049605745995415574))
@app_commands.describe(nom_localite="Nom de la ville")
@app_commands.autocomplete(nom_localite=enabled_cities_autocomplete)
async def stop_weather(interaction : discord.Interaction, nom_localite : str):
  await controller.stop_weather(interaction, nom_localite)



#####################################################################################################
#ALWAYS RUN PART - DO NOT PUT ANYTHING BELOW - ALWAYS RUN PART - DO NOT PUT ANYTHING BELOW 
#####################################################################################################

phyxit.run(os.environ["PHYXIT_BOT_TOKEN"])