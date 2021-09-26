from discord.ext import commands
import discord
import matplotlib.pyplot as plt
import os
import pyimgur
import datetime
import asyncio
from discordbot import bot_colour, gst_bot
import config_discordbot as cfg
from helpers import pagination

im = pyimgur.Imgur(cfg.IMGUR_CLIENT_ID)


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
    "": "Sector",
}


def img_path_exists_and_correction(img_path, time):
    if not os.path.exists(img_path):
        time = time - datetime.timedelta(seconds=1)
        img_path = os.path.join(
            cfg.gst_path,
            "exports",
            "economy",
            f"feargreed_{time.strftime('%Y%m%d_%H%M%S')}.png",
        )
    return img_path, time


def feargreed_command():
    plt.ion()
    fig = plt.figure(figsize=[1, 1], dpi=10)
    report, _ = cnn_model.get_feargreed_report("", fig)
    cnn_view.fear_and_greed_index(indicator="", export="png")
    plt.close("all")
    now = datetime.datetime.now()
    image_path = os.path.join(
        cfg.gst_path,
        "exports",
        "economy",
        f"feargreed_{now.strftime('%Y%m%d_%H%M%S')}.png",
    )
    if not os.path.exists(image_path):
        time = now + datetime.timedelta(seconds=1)
        img_path = os.path.join(
            cfg.gst_path,
            "exports",
            "economy",
            f"feargreed_{now.strftime('%Y%m%d_%H%M%S')}.png",
        )
    i = 0
    while not os.path.exists(image_path) and i < 10:
        image_path, now = img_path_exists_and_correction(image_path, now)
        i += 1
    try:
        uploaded_image = im.upload_image(image_path, title="something")
    except:
        report = "Error: The image could not be found"
        print("Error with uploading the the image to Imgur.")
        image_link = uploaded_image.link
        embed = discord.Embed(
            title="CNN Fear Geed Index", description=report, colour=bot_colour
        )
        embed.set_author(
            name="Gamestonk Terminal",
            icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
        )
        return embed
    uploaded_image = im.upload_image(image_path, title="something")
    image_link = uploaded_image.link
    embed = discord.Embed(
        title="CNN Fear Geed Index", description=report, colour=bot_colour
    )
    embed.set_author(
        name="Gamestonk Terminal",
        icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
    )
    embed.set_image(url=image_link)
    plt.close("all")
    return embed


def overview_command():
    df_data = wsj_model.market_overview()
    if df_data.empty:
        df_data_str = "No overview data available"
    else:
        df_data_str = "```" + df_data.to_string(index=False) + "```"
    embed = discord.Embed(
        title="WSJ Market Overview", description=df_data_str, colour=bot_colour
    )
    embed.set_author(
        name="Gamestonk Terminal",
        icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
    )
    return embed


def indices_command():
    df_data = wsj_model.us_indices()
    if df_data.empty:
        df_data_str = "No indices data available"
    else:
        df_data_str = "```" + df_data.to_string(index=False) + "```"
    embed = discord.Embed(
        title="WSJ US Indices", description=df_data_str, colour=bot_colour
    )
    embed.set_author(
        name="Gamestonk Terminal",
        icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
    )
    return embed


def futures_command():
    df_data = wsj_model.top_commodities()
    if df_data.empty:
        df_data_str = "No futures/commodities data available"
    else:
        df_data_str = "```" + df_data.to_string(index=False) + "```"
    embed = discord.Embed(
        title="WSJ Futures/Commodities", description=df_data_str, colour=bot_colour
    )
    embed.set_author(
        name="Gamestonk Terminal",
        icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
    )
    return embed


def usbonds_command():
    df_data = wsj_model.us_bonds()
    if df_data.empty:
        df_data_str = "No US bonds data available"
    else:
        df_data_str = "```" + df_data.to_string(index=False) + "```"
    embed = discord.Embed(
        title="WSJ US Bonds", description=df_data_str, colour=bot_colour
    )
    embed.set_author(
        name="Gamestonk Terminal",
        icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
    )
    return embed


def glbonds_command():
    df_data = wsj_model.global_bonds()
    if df_data.empty:
        df_data_str = "No global bonds data available"
    else:
        df_data_str = "```" + df_data.to_string(index=False) + "```"
    embed = discord.Embed(
        title="WSJ Global Bonds", description=df_data_str, colour=bot_colour
    )
    embed.set_author(
        name="Gamestonk Terminal",
        icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
    )
    return embed


def currencies_command():
    df_data = wsj_model.global_currencies()
    if df_data.empty:
        df_data_str = "No currencies data available"
    else:
        df_data_str = "```" + df_data.to_string(index=False) + "```"
    embed = discord.Embed(
        title="WSJ Currencies", description=df_data_str, colour=bot_colour
    )
    embed.set_author(
        name="Gamestonk Terminal",
        icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
    )
    return embed


async def valuation_command(ctx, arg):
    sector = economy_dict[arg]
    df_group = finviz_model.get_valuation_performance_data(sector, "valuation")
    future_column_name = df_group["Name"]
    df_group = df_group.transpose()
    df_group.columns = future_column_name
    df_group.drop("Name")
    columns = []
    initial_str = "Page 1: Overview"
    i = 2
    current = 0
    for column in df_group.columns.values:
        initial_str = initial_str + "\nPage " + str(i) + ": " + column
        i += 1
    columns.append(
        discord.Embed(
            title="Finviz " + sector + " Valuation",
            description=initial_str,
            colour=bot_colour,
        ).set_author(
            name="Gamestonk Terminal",
            icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
        )
    )
    for column in df_group.columns.values:
        columns.append(
            discord.Embed(
                description="```" + df_group[column].fillna("").to_string() + "```",
                colour=bot_colour,
            ).set_author(
                name="Gamestonk Terminal",
                icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
            )
        )

    await pagination(columns, ctx)


async def performance_command(ctx, arg):
    sector = economy_dict[arg]
    df_group = finviz_model.get_valuation_performance_data(sector, "performance")
    future_column_name = df_group["Name"]
    df_group = df_group.transpose()
    df_group.columns = future_column_name
    df_group.drop("Name")
    columns = []
    initial_str = "Page 1: Overview"
    i = 2
    current = 0
    for column in df_group.columns.values:
        initial_str = initial_str + "\nPage " + str(i) + ": " + column
        i += 1
    columns.append(
        discord.Embed(
            title="Finviz " + sector + " Performance",
            description=initial_str,
            colour=bot_colour,
        ).set_author(
            name="Gamestonk Terminal",
            icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
        )
    )
    for column in df_group.columns.values:
        columns.append(
            discord.Embed(
                description="```" + df_group[column].fillna("").to_string() + "```",
                colour=bot_colour,
            ).set_author(
                name="Gamestonk Terminal",
                icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
            )
        )

    await pagination(columns, ctx)


class EconomyCommands(commands.Cog):
    """A couple of economy commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="economy.feargreed")
    async def feargreed(self, ctx: commands.Context):
        embed = feargreed_command()
        await ctx.send(embed=embed)

    @commands.command(name="economy.overview")
    async def overview(self, ctx: commands.Context):
        embed = overview_command()
        await ctx.send(embed=embed)

    @commands.command(name="economy.indices")
    async def indices(self, ctx: commands.Context):
        embed = indices_command()
        await ctx.send(embed=embed)

    @commands.command(name="economy.futures")
    async def futures(self, ctx: commands.Context):
        embed = futures_command()
        await ctx.send(embed=embed)

    @commands.command(name="economy.usbonds")
    async def usbonds(self, ctx: commands.Context):
        embed = usbonds_command()
        await ctx.send(embed=embed)

    @commands.command(name="economy.glbonds")
    async def glbonds(self, ctx: commands.Context):
        embed = glbonds_command()
        await ctx.send(embed=embed)

    @commands.command(name="economy.currencies")
    async def currencies(self, ctx: commands.Context):
        embed = currencies_command()
        await ctx.send(embed=embed)

    @commands.command(name="economy.valuation")
    async def valuation(self, ctx: commands.Context, arg):
        await valuation_command(ctx, arg)

    @commands.command(name="economy.performance")
    async def performance(self, ctx: commands.Context, arg):
        await performance_command(ctx, arg)

    @commands.command(name="economy")
    async def economy(self, ctx: commands.Context):
        text = (
            "0️⃣ !economy.overview\n\n1️⃣ !economy.futures\n\n2️⃣ !economy.usbonds\n\n3️⃣ !economy.glbonds\n\n4️⃣ !economy.indices"
            "\n\n5️⃣ !economy.currencies\n\n6️⃣ !economy.feargreed\n\n7️⃣ !economy.valuation SECTOR (default: sector)\n\n8️⃣ !economy.performance SECTOR (default: sector)"
        )

        title = "Economy Menu"
        embed = discord.Embed(title=title, description=text, colour=bot_colour)
        embed.set_author(
            name="Gamestonk Terminal",
            icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
        )
        msg = await ctx.send(embed=embed)

        emoji_list = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]

        await msg.add_reaction("0️⃣")
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        await msg.add_reaction("3️⃣")
        await msg.add_reaction("4️⃣")
        await msg.add_reaction("5️⃣")
        await msg.add_reaction("6️⃣")
        await msg.add_reaction("7️⃣")
        await msg.add_reaction("8️⃣")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in emoji_list

        try:
            reaction, user = await gst_bot.wait_for("reaction_add", timeout=10, check=check)
            if reaction.emoji == "0️⃣":
                embed = overview_command()
                await ctx.send(embed=embed)
            elif reaction.emoji == "1️⃣":
                embed = futures_command()
                await ctx.send(embed=embed)
            elif reaction.emoji == "2️⃣":
                embed = usbonds_command()
                await ctx.send(embed=embed)
            elif reaction.emoji == "3️⃣":
                embed = glbonds_command()
                await ctx.send(embed=embed)
            elif reaction.emoji == "4️⃣":
                embed = indices_command()
                await ctx.send(embed=embed)
            elif reaction.emoji == "5️⃣":
                embed = currencies_command()
                await ctx.send(embed=embed)
            elif reaction.emoji == "6️⃣":
                embed = feargreed_command()
                await ctx.send(embed=embed)
            elif reaction.emoji == "7️⃣":
                await valuation_command(ctx, "")
            elif reaction.emoji == "8️⃣":
                await performance_command(ctx, "")
        except asyncio.TimeoutError:
            text = text + "\n\nCommand timeout."
            embed = discord.Embed(title=title, description=text)
            await msg.edit(embed=embed)


def setup(bot: commands.Bot):
    gst_bot.add_cog(EconomyCommands(bot))
