from discord.ext import commands
import discord
from helpers import pagination
from discordbot import gst_bot
import config_discordbot as cfg
import helpers
import os
import asyncio
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pyimgur

im = pyimgur.Imgur(cfg.IMGUR_CLIENT_ID)

from gamestonk_terminal.stocks.dark_pool_shorts import stockgrid_model

from gamestonk_terminal.config_plot import PLOT_DPI

from stocks.dark_pool_shorts.shorted import shorted_command
from stocks.dark_pool_shorts.ftd import ftd_command
from stocks.dark_pool_shorts.dpotc import dpotc_command
from stocks.dark_pool_shorts.spos import spos_command
from stocks.dark_pool_shorts.psi import psi_command
from stocks.dark_pool_shorts.hsi import hsi_command
from stocks.dark_pool_shorts.pos import pos_command
from stocks.dark_pool_shorts.sidtc import sidtc_command


class DarkPoolShortsCommands(commands.Cog):
    """Dark Pool Shorts menu."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="stocks.dps.shorted")
    async def shorted(self, ctx: commands.Context, arg=""):
        if arg:
            await shorted_command(ctx, arg)
        else:
            await shorted_command(ctx)

    @commands.command(name="stocks.dps.ftd")
    async def ftd(self, ctx: commands.Context, arg, arg2="", arg3=""):
        if arg2:
            if arg3:
                embed = ftd_command(arg, arg2, arg3)
            else:
                embed = ftd_command(arg, arg2)
        else:
            if arg3:
                embed = ftd_command(arg, arg3=arg3)
            else:
                embed = ftd_command(arg)
        await ctx.send(embed=embed)

    @commands.command(name="stocks.dps.dpotc")
    async def dpotc(self, ctx: commands.Context, arg, arg2="", arg3=""):
        if arg2:
            if arg3:
                embed = dpotc_command(arg, arg2, arg3)
            else:
                embed = dpotc_command(arg, arg2)
        else:
            if arg3:
                embed = dpotc_command(arg, arg3=arg3)
            else:
                embed = dpotc_command(arg)
        await ctx.send(embed=embed)

    @commands.command(name="stocks.dps.spos")
    async def spos(self, ctx: commands.Context, arg):
        embed = spos_command(arg)
        await ctx.send(embed=embed)

    @commands.command(name="stocks.dps.psi")
    async def psi(self, ctx: commands.Context, arg):
        embed = psi_command(arg)
        await ctx.send(embed=embed)

    @commands.command(name="stocks.dps.hsi")
    async def hsi(self, ctx: commands.Context, arg="10"):
        arg = int(arg)
        await hsi_command(ctx, arg)

    @commands.command(name="stocks.dps.pos")
    async def pos(self, ctx: commands.Context, arg="10", arg2="dpp_dollar"):
        arg = int(arg)
        await pos_command(ctx, arg, arg2)

    @commands.command(name="stocks.dps.sidtc")
    async def sidtc(self, ctx: commands.Context, arg="10", arg2="float"):
        arg = int(arg)
        await sidtc_command(ctx, arg, arg2)

    @commands.command(name="stocks.dps")
    async def dark_pool_shorts_menu(self, ctx: commands.Context):
        text = (
            "0️⃣ !stocks.dps.shorted NUM (default: 5)\n\n1️⃣ !stocks.dps.hsi NUM (default: 10)\n\n2️⃣ !stocks.dps.pos NUM "
            "(default: 10) SORT (default: dpp_dollar; options: sv,sv_pct,nsv,nsv_dollar,dpp,dpp_dollar)\n\n3️⃣ "
            "!stocks.dps.sidtc NUM (default: 10) SORT (default: float; options: float,dtc,si)\n\nCommands below "
            "require the input TICKER and must be entered directly:\n(DATE format: "
            ")\n\n4️⃣"
            "!stocks.dps.ftd TICKER DATE_START DATE_END\n\n5️⃣ !stocks.dps.dpotc TICKER DATE_START DATE_END\n\n6️⃣ "
            "!stocks.dps.spos TICKER\n\n7️⃣ !stocks.dps.psi TICKER"
        )

        title = "Dark Pool Shorts (DPS) Menu"
        embed = discord.Embed(title=title, description=text, colour=cfg.COLOR)
        embed.set_author(
            name=cfg.AUTHOR_NAME,
            icon_url=cfg.AUTHOR_ICON_URL,
        )
        msg = await ctx.send(embed=embed)

        emoji_list = ["0️⃣", "1️⃣", "2️⃣", "3️⃣"]

        await msg.add_reaction("0️⃣")
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        await msg.add_reaction("3️⃣")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in emoji_list

        try:
            reaction, user = await gst_bot.wait_for(
                "reaction_add", timeout=10, check=check
            )
            if reaction.emoji == "0️⃣":
                await shorted_command(ctx, 5)
            elif reaction.emoji == "1️⃣":
                await hsi_command(ctx, 10)
            elif reaction.emoji == "2️⃣":
                await pos_command(ctx, 10, "dpp_dollar")
            elif reaction.emoji == "3️⃣":
                await sidtc_command(ctx, 10, "float")

        except asyncio.TimeoutError:
            text = text + "\n\nCommand timeout."
            embed = discord.Embed(title=title, description=text)
            await msg.edit(embed=embed)


def setup(bot: commands.Bot):
    gst_bot.add_cog(DarkPoolShortsCommands(bot))
