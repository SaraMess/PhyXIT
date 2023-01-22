#**************************************************#
#                 main.pyFile                      #
#**************************************************#
#   Authors : Sara MESSARA - Clément PAGES         #
#**************************************************#


#========================================#
#       Modules used in this file        #
#========================================#

import ast
import discord
from discord.ext import commands
from discord import app_commands
import logging
import paho.mqtt.client as mqtt
import os
import typing

from BotController import BotController, FREQ_MINUTES



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
  for city_choice in await controller.get_city_list():
    if current.lower() in city_choice.lower():
      choices_list.append(app_commands.Choice(name=city_choice, value=city_choice))
  return choices_list


async def enabled_cities_autocomplete(interaction : discord.Interaction, current : str) -> typing.List[app_commands.Choice[str]]:
  choices_list = []
  for city_choice in await controller.get_enabled_cities_list():
    if current.lower() in city_choice.lower():
      choices_list.append(app_commands.Choice(name=city_choice, value=city_choice))
  return choices_list


async def available_esp_data_type_autocomplete(interaction : discord.Interaction, current : str) -> typing.List[app_commands.Choice[str]]:
  choices_list = []
  for data_type_choice in controller.get_available_data_type():
    if current.lower() in data_type_choice.lower():
      choices_list.append(app_commands.Choice(name=data_type_choice, value=data_type_choice))
  choices_list.append(app_commands.Choice(name="all", value="all"))
  return choices_list


@phyxit.tree.command(name="ping", description="Si je suis réveillé, je réponds pong! Sinon... et bien c'est que je dors 😴", guild=discord.Object(id=1049605745995415574))
async def ping(interaction : discord.Interaction):
  await controller.ping(interaction)


@phyxit.tree.command(name="ajoute_ville", description="Ajoute une ville pour laquelle vous souhaitez obtenir la météo, dans la limite de 6 villes", guild=discord.Object(id=1049605745995415574))
@app_commands.describe(nom_localite="Nom de la ville à ajouter")
async def ajouterVille(interaction : discord.Interaction, nom_localite : str):
  await controller.add_city(interaction, nom_localite.capitalize())


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


@phyxit.tree.command(name="info", description="Indique les villes connues par le bot", guild=discord.Object(id=1049605745995415574))
async def get_cities_status(interaction : discord.Interaction):
  await controller.get_cities_status(interaction)


@phyxit.tree.command(name="esp32", description="Data en provenance de l'ESP32", guild=discord.Object(id=1049605745995415574))
@app_commands.describe(type_donnees="type de données à afficher")
@app_commands.autocomplete(type_donnees=available_esp_data_type_autocomplete)
async def get_stats(interaction : discord.Interaction, type_donnees : str):
  await controller.get_esp32_data(interaction, type_donnees)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    res, _ = client.subscribe("esp32/sensors")
    print("sub res = ", res)
    client.subscribe("esp32/presence")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logging.info(f"receive data from {msg.topic}: {str(msg.payload)}")
    topic = msg.topic
    dict_msg = ast.literal_eval(msg.payload.decode("utf-8"))
    if topic == "esp32/sensors":
      for sensor in dict_msg["Sensors"].keys():
        input_sensor_values = [val / 1000 for val in dict_msg["Sensors"][sensor]]
        controller.mqtt_data[sensor].extend(input_sensor_values)
    elif topic == "esp32/presence":
      pass



hostname = "51.178.50.237"
client = mqtt.Client("upssitech")
client.on_connect = on_connect # assign the ack callback
client.on_message = on_message
client.username_pw_set("upssitech", password="2011")
client.connect(hostname, 1883, 60)
client.loop_start()


#####################################################################################################
#ALWAYS RUN PART - DO NOT PUT ANYTHING BELOW - ALWAYS RUN PART - DO NOT PUT ANYTHING BELOW 
#####################################################################################################

phyxit.run(os.environ["PHYXIT_BOT_TOKEN"])