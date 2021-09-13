from discord.ext import commands
import discord
import matplotlib.pyplot as plt
import sys
import os
import pyimgur
import datetime
import math
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
        "capitalization": "Capitalization",
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
        print(sector)
        df_group = finviz_model.get_valuation_performance_data(sector, "valuation")
        df_group_str = df_group.fillna("").to_string(index=False)
        df_group_str_perm = df_group_str
        if len(df_group_str) > 4050:
            df_group_str = "```" + df_group_str[:4049] + "```"
            too_long = True
        else:
            df_group_str = "```" + df_group_str + "\n\n...```"
            too_long = False
        title = "Finviz " + sector + " Valuation"
        embed = discord.Embed(title=title, description=df_group_str, colour=bot_colour)
        embed.set_author(name="Gamestonk Terminal",
                         icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true")
        await ctx.send(embed=embed)
        if too_long:
            times = math.ceil((len(df_group_str_perm)/4050)-1)
            i = 1
            char_num = 4050
            char_num_upper = 8100
            while times >= i:
                title = "Finviz " + sector + " Valuation Part " + str(i+1)
                if i == times:
                    df_group_str = "``` ...\n" + df_group_str_perm[char_num:] + "```"
                else:
                    df_group_str = "``` ...\n" + df_group_str_perm[char_num:char_num_upper] + "```"
                embed = discord.Embed(title=title, description=df_group_str, colour=bot_colour)
                embed.set_author(name="Gamestonk Terminal",
                                 icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true")
                await ctx.send(embed=embed)
                i += 1
                char_num = char_num_upper
                char_num_upper += 4050


def setup(bot: commands.Bot):
    bot.add_cog(EconomyCommands(bot))
