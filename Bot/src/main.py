#Importation des différents modules
import os
import discord
from discord.ext import commands
import threading
import json
import requests
import numpy as np
import time
from PIL import Image
import logging
from VisualCrossingHandler import VisualCrossingHandler


#=======================
#    GLOBAL VARIABLES
#=======================

#Declare a bot instance :
phyxit = commands.Bot(command_prefix='+', intents=discord.Intents.all())
vc_handler = VisualCrossingHandler()
#Declare a logger for debugging purposes:
logging.basicConfig(level=logging.INFO)




#==================================
#        BOT EVENTS
#==================================


@phyxit.event
async def on_ready():
    vc_handler.start()
    logging.info("Bot is ready to use!")




@phyxit.event
async def on_message(message):
    logging.info("A message was received")
    await phyxit.process_commands(message)
    #TODO Add event handler



#====================
#    BOT'S COMMANDS
#====================



@phyxit.command(name="ping", brief="Test command to see if the bot is alive")
async def ping(ctx):
  await ctx.channel.send("pong !")


#####################################################################################################
#ALWAYS RUN PART - DO NOT PUT ANYTHING BELOW - ALWAYS RUN PART - DO NOT PUT ANYTHING BELOW 
#####################################################################################################

phyxit.run("MTA0OTYxMTk0OTUyMjAyNjUxNg.GAjQUa.w4UbRBs1zb7uGlPUkFU0XLp0FxxjL1icaSSvxQ")