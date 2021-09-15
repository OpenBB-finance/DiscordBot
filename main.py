import discord
from discord import Client, Intents, Embed
from discord.ext import commands
import sys
import os
import pathlib

##############
## Settings ##
##############
DISCORD_BOT_TOKEN = 'string' # Insert your bots secrets token
IMGUR_CLIENT_ID = 'string' # Enter your imgur client id
command_prefix = '!' # Sets the prefix to the commands
activity = discord.Game(name='Gametonk Terminal: https://github.com/GamestonkTerminal/GamestonkTerminal')
gst_path = 'C:\\Users\\user\\GamestonkTerminal' # The path to Gamestonk Terminal

## Defining the bot ##
bot = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all(), activity=activity)

sys.path.append(gst_path)

bot_colour = discord.Color.from_rgb(0, 206, 154)

## Loads the commands (Cogs) from each "context" ##
bot.load_extension("general_commands")
bot.load_extension("economy_commands")

## Runs the bot ##
bot.run(DISCORD_BOT_TOKEN)

