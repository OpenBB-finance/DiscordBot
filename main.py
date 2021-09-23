import discord
from discord import Client, Intents, Embed
from discord.ext import commands
import sys
import os
import pathlib
from discord_components import DiscordComponents, Button, ButtonStyle
import asyncio

##############
## Settings ##
##############
DISCORD_BOT_TOKEN = 'string' # Insert your bots secrets token
IMGUR_CLIENT_ID = 'string' # Enter your imgur client id
command_prefix = '!' # Sets the prefix to the commands
activity = discord.Game(name='Gametonk Terminal: https://github.com/GamestonkTerminal/GamestonkTerminal')
gst_path = 'C:\\Users\\user\\GamestonkTerminal' # The path to Gamestonk Terminal
date_input_format = '%Y-%m-%d' # Enter your prefered date input format

## Defining the bot ##
bot = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all(), activity=activity)
DiscordComponents(bot)

bot_colour = discord.Color.from_rgb(0, 206, 154)

sys.path.append(gst_path)

async  def pagination(dataset_with_embeds, ctx):
    current = 0
    components = [[Button(label="Prev", id="back", style=ButtonStyle.red),
                   Button(label=f"Page {int(dataset_with_embeds.index(dataset_with_embeds[current]))}/{len(dataset_with_embeds)}",
                          id="cur", style=ButtonStyle.green, disabled=True),
                   Button(label="Next", id="front", style=ButtonStyle.green)]]
    mainMessage = await ctx.send(embed=dataset_with_embeds[current], components=components)
    while True:
        # Try and except blocks to catch timeout and break
        try:
            interaction = await bot.wait_for(
                "button_click",
                check=lambda i: i.component.id in ["back", "front"],  # You can add more
                timeout=30.0  # 30 seconds of inactivity
            )
            # Getting the right list index
            if interaction.component.id == "back":
                current -= 1
            elif interaction.component.id == "front":
                current += 1
            # If its out of index, go back to start / end
            if current == len(dataset_with_embeds):
                current = 0
            elif current < 0:
                current = len(dataset_with_embeds) - 1

            # Edit to new page + the center counter changes
            components = [[Button(label="Prev", id="back", style=ButtonStyle.red),
                           Button(
                               label=f"Page {int(dataset_with_embeds.index(dataset_with_embeds[current]))}/{len(dataset_with_embeds)}",
                               id="cur", style=ButtonStyle.green, disabled=True),
                           Button(label="Next", id="front", style=ButtonStyle.green)]]

            await interaction.edit_origin(
                embed=dataset_with_embeds[current],
                components=components
            )
        except asyncio.TimeoutError:
            # Disable and get outta here
            components = [[Button(label="Prev", id="back", style=ButtonStyle.green, disabled=True),
                           Button(label=f"Page {int(dataset_with_embeds.index(dataset_with_embeds[current])) + 1}/{len(dataset_with_embeds)}",
                                  id="cur", style=ButtonStyle.grey, disabled=True),
                           Button(label="Next", id="front", style=ButtonStyle.green, disabled=True)]]
            await mainMessage.edit(
                components=components
            )
            break

async def on_ready():
    print("Bot Online")

## Loads the commands (Cogs) from each "context" ##
bot.load_extension("general_commands")
bot.load_extension("economy_commands")
bot.load_extension("stocks.dark_pool_shorts")

## Runs the bot ##
bot.run(DISCORD_BOT_TOKEN)
