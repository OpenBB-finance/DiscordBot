from discord.ext import commands
import discord
from discord_components import Button, ButtonStyle
import matplotlib.pyplot as plt
import sys
import os
import pyimgur
import datetime
import math
import asyncio
from main import gst_path, IMGUR_CLIENT_ID, bot_colour, command_prefix, bot

im = pyimgur.Imgur(IMGUR_CLIENT_ID)
sys.path.append(gst_path)

from gamestonk_terminal.economy import cnn_view, cnn_model, wsj_model, finviz_model

economy_dict = {
        "sector": "Sector",
        "industry": "Industry",
        "basic materials": "Industry (Basic Materials)",
        "communication services": "Industry (Communication Services)",
        "consumer cyclical": "Industry (Consumer Cyclical)",
        "consumer defensive": "Industry (Consumer Defensive)",
        "energy": "Industry (Energy)",
        "financial": "Industry (Financial)",
        "healthcare": "Industry (Healthcare)",
        "industrials": "Industry (Industrials)",
        "real Estate": "Industry (Real Estate)",
        "technology": "Industry (Technology)",
        "utilities": "Industry (Utilities)",
        "country": "Country (U.S. listed stocks only)",
        "capitalization": "Capitalization"
    }

def img_path_exists_and_correction(img_path, time):
    if not os.path.exists(img_path):
        time = time - datetime.timedelta(seconds=1)
        img_path = os.path.join(gst_path, 'exports', 'economy', f"feargreed_{time.strftime('%Y%m%d_%H%M%S')}.png")
    return img_path, time

class EconomyCommands(commands.Cog):
    """A couple of economy commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='feargreed')
    async def feargreed(self, ctx: commands.Context):
        plt.ion()
        fig = plt.figure(figsize=[1,1], dpi=10)
        report, _ = cnn_model.get_feargreed_report('', fig)
        cnn_view.fear_and_greed_index(indicator='', export='png')
        plt.close('all')
        now = datetime.datetime.now()
        image_path = os.path.join(gst_path, 'exports', 'economy', f"feargreed_{now.strftime('%Y%m%d_%H%M%S')}.png")
        if not os.path.exists(image_path):
            time = now + datetime.timedelta(seconds=1)
            img_path = os.path.join(gst_path, 'exports', 'economy', f"feargreed_{now.strftime('%Y%m%d_%H%M%S')}.png")
        i = 0
        while not os.path.exists(image_path) and i < 10:
            image_path, now = img_path_exists_and_correction(image_path, now)
            i += 1
        try:
            uploaded_image = im.upload_image(image_path, title='something')
        except:
            report = "Error: The image could not be found"
            print("Error with uploading the the image to Imgur.")
            image_link = uploaded_image.link
            embed = discord.Embed(title='CNN Fear Geed Index', description=report, colour=bot_colour)
            embed.set_author(name="Gamestonk Terminal",
                             icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true")
            await ctx.send(embed=embed)
            return
        uploaded_image = im.upload_image(image_path, title='something')
        image_link = uploaded_image.link
        embed = discord.Embed(title='CNN Fear Geed Index', description=report, colour=bot_colour)
        embed.set_author(name="Gamestonk Terminal",
                         icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true")
        embed.set_image(url=image_link)
        plt.close('all')
        await ctx.send(embed=embed)

    @commands.command(name='overview')
    async def overview(self, ctx: commands.Context):
        df_data = wsj_model.market_overview()
        if df_data.empty:
            df_data_str = "No overview data available"
        else:
            df_data_str = "```" + df_data.to_string(index=False) + "```"
        embed = discord.Embed(title="WSJ Market Overview", description=df_data_str, colour=bot_colour)
        embed.set_author(name="Gamestonk Terminal",
                         icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true")
        await ctx.send(embed=embed)

    @commands.command(name='indices')
    async def indices(self, ctx: commands.Context):
        df_data = wsj_model.us_indices()
        if df_data.empty:
            df_data_str = "No indices data available"
        else:
            df_data_str = "```" + df_data.to_string(index=False) + "```"
        embed = discord.Embed(title="WSJ US Indices", description=df_data_str, colour=bot_colour)
        embed.set_author(name="Gamestonk Terminal",
                         icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true")
        await ctx.send(embed=embed)

    @commands.command(name='futures')
    async def futures(self, ctx: commands.Context):
        df_data = wsj_model.top_commodities()
        if df_data.empty:
            df_data_str = "No futures/commodities data available"
        else:
            df_data_str = "```" + df_data.to_string(index=False) + "```"
        embed = discord.Embed(title="WSJ Futures/Commodities", description=df_data_str, colour=bot_colour)
        embed.set_author(name="Gamestonk Terminal",
                         icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true")
        await ctx.send(embed=embed)

    @commands.command(name='usbonds')
    async def usbonds(self, ctx: commands.Context):
        df_data = wsj_model.us_bonds()
        if df_data.empty:
            df_data_str = "No US bonds data available"
        else:
            df_data_str = "```" + df_data.to_string(index=False) + "```"
        embed = discord.Embed(title="WSJ US Bonds", description=df_data_str, colour=bot_colour)
        embed.set_author(name="Gamestonk Terminal",
                         icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true")
        await ctx.send(embed=embed)

    @commands.command(name='glbonds')
    async def glbonds(self, ctx: commands.Context):
        df_data = wsj_model.global_bonds()
        if df_data.empty:
            df_data_str = "No global bonds data available"
        else:
            df_data_str = "```" + df_data.to_string(index=False) + "```"
        embed = discord.Embed(title="WSJ Global Bonds", description=df_data_str, colour=bot_colour)
        embed.set_author(name="Gamestonk Terminal",
                         icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true")
        await ctx.send(embed=embed)

    @commands.command(name='currencies')
    async def currencies(self, ctx: commands.Context):
        df_data = wsj_model.global_currencies()
        if df_data.empty:
            df_data_str = "No currencies data available"
        else:
            df_data_str = "```" + df_data.to_string(index=False) + "```"
        embed = discord.Embed(title="WSJ Currencies", description=df_data_str, colour=bot_colour)
        embed.set_author(name="Gamestonk Terminal",
                         icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true")
        await ctx.send(embed=embed)

    @commands.command(name='valuation')
    async def valuation(self, ctx: commands.Context, arg):
        sector = economy_dict[arg]
        df_group = finviz_model.get_valuation_performance_data(sector, "valuation")
        future_column_name = df_group['Name']
        df_group = df_group.transpose()
        df_group.columns = future_column_name
        df_group.drop('Name')
        columns = []
        initial_str = "Page 1: Overview"
        i = 2
        current = 0
        for column in df_group.columns.values:
            initial_str = initial_str + "\nPage " + str(i) + ": " + column
            i += 1
        columns.append(discord.Embed(title = "Finviz " + sector + " Valuation", description=initial_str, colour=bot_colour).set_author(name="Gamestonk Terminal",
                         icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true"))
        for column in df_group.columns.values:
            columns.append(discord.Embed(description="```" + df_group[column].fillna("").to_string() + "```",
                                         colour=bot_colour).set_author(name="Gamestonk Terminal",
                         icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true"))

        components = [[Button(label="Prev", id="back", style=ButtonStyle.red),
            Button(label=f"Page {int(columns.index(columns[current]))}/{len(columns)}",
                   id="cur", style=ButtonStyle.green, disabled=True),
            Button(label="Next", id="front", style=ButtonStyle.green)]]
        mainMessage = await ctx.send(embed=columns[current], components=components)
        while True:
            # Try and except blocks to catch timeout and break
            try:
                interaction = await bot.wait_for(
                    "button_click",
                    check=lambda i: i.component.id in ["back", "front"],  # You can add more
                    timeout=20.0  # 20 seconds of inactivity
                )
                # Getting the right list index
                if interaction.component.id == "back":
                    current -= 1
                elif interaction.component.id == "front":
                    current += 1
                # If its out of index, go back to start / end
                if current == len(columns):
                    current = 0
                elif current < 0:
                    current = len(columns) - 1

                # Edit to new page + the center counter changes
                components = [[Button(label="Prev", id="back", style=ButtonStyle.red),
                               Button(
                                   label=f"Page {int(columns.index(columns[current]))}/{len(columns)}",
                                   id="cur", style=ButtonStyle.green, disabled=True),
                               Button(label="Next", id="front", style=ButtonStyle.green)]]

                await interaction.edit_origin(
                    embed=columns[current],
                    components=components
                )
            except asyncio.TimeoutError:
                # Disable and get outta here
                components = [[Button(label="Prev", id="back", style=ButtonStyle.green, disabled=True),
                               Button(label=f"Page {int(columns.index(columns[current])) + 1}/{len(columns)}",
                                    id="cur", style=ButtonStyle.grey, disabled=True),
                               Button(label="Next", id="front", style=ButtonStyle.green, disabled=True)]]
                await mainMessage.edit(
                    components=components
                )
                break


def setup(bot: commands.Bot):
    bot.add_cog(EconomyCommands(bot))
    
