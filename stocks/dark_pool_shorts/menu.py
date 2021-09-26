import discord
from discordbot import gst_bot
import config_discordbot as cfg
import asyncio

from stocks.dark_pool_shorts.shorted import shorted_command
from stocks.dark_pool_shorts.ftd import ftd_command
from stocks.dark_pool_shorts.dpotc import dpotc_command
from stocks.dark_pool_shorts.spos import spos_command
from stocks.dark_pool_shorts.psi import psi_command
from stocks.dark_pool_shorts.hsi import hsi_command
from stocks.dark_pool_shorts.pos import pos_command
from stocks.dark_pool_shorts.sidtc import sidtc_command


class DarkPoolShortsCommands(discord.ext.commands.Cog):
    """Dark Pool Shorts menu."""

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @discord.ext.commands.command(name="stocks.dps.shorted")
    async def shorted(self, ctx: discord.ext.commands.Context, arg=""):
        await shorted_command(ctx, arg)

    @discord.ext.commands.command(name="stocks.dps.hsi")
    async def hsi(self, ctx: discord.ext.commands.Context, arg=""):
        await hsi_command(ctx, arg)

    @discord.ext.commands.command(name="stocks.dps.pos")
    async def pos(self, ctx: discord.ext.commands.Context, arg="10", arg2="dpp_dollar"):
        arg = int(arg)
        await pos_command(ctx, arg, arg2)

    @discord.ext.commands.command(name="stocks.dps.sidtc")
    async def sidtc(self, ctx: discord.ext.commands.Context, arg="10", arg2="float"):
        arg = int(arg)
        await sidtc_command(ctx, arg, arg2)

    @discord.ext.commands.command(name="stocks.dps.ftd")
    async def ftd(self, ctx: discord.ext.commands.Context, arg, arg2="", arg3=""):
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

    @discord.ext.commands.command(name="stocks.dps.dpotc")
    async def dpotc(self, ctx: discord.ext.commands.Context, arg, arg2="", arg3=""):
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

    @discord.ext.commands.command(name="stocks.dps.spos")
    async def spos(self, ctx: discord.ext.commands.Context, arg):
        embed = spos_command(arg)
        await ctx.send(embed=embed)

    @discord.ext.commands.command(name="stocks.dps.psi")
    async def psi(self, ctx: discord.ext.commands.Context, arg):
        embed = psi_command(arg)
        await ctx.send(embed=embed)

    # !stocks.dps.pos <NUM> (default: 10) SORT (default: dpp_dollar; options: sv,sv_pct,nsv,nsv_dollar,dpp,dpp_dollar
    # !stocks.dps.sidtc NUM (default: 10) SORT (default: float; options: float,dtc,si)

    @discord.ext.commands.command(name="stocks.dps")
    async def dark_pool_shorts_menu(self, ctx: discord.ext.commands.Context, arg=""):
        text = (
            "0️⃣ !stocks.dps.shorted <NUM>\n"
            "1️⃣ !stocks.dps.hsi <NUM>\n"
            "2️⃣ !stocks.dps.pos <NUM> <SORT>\n"
            "3️⃣ !stocks.dps.sidtc <NUM> <SORT>\n"
        )
        if arg:
            text += (
                "4️⃣ !stocks.dps.ftd <TICKER> <DATE_START> <DATE_END>\n"
                "5️⃣ !stocks.dps.dpotc <TICKER> <DATE_START> <DATE_END>\n"
                "6️⃣ !stocks.dps.spos <TICKER>\n"
                "7️⃣ !stocks.dps.psi <TICKER>\n"
            )
        else:
            text += (
                "\nMore commands available when providing a ticker with:"
                "\n!stocks.dps <TICKER>"
            )

        title = "Dark Pool Shorts (DPS) Menu"
        embed = discord.Embed(title=title, description=text, colour=cfg.COLOR)
        embed.set_author(
            name=cfg.AUTHOR_NAME,
            icon_url=cfg.AUTHOR_ICON_URL,
        )
        msg = await ctx.send(embed=embed)

        emoji_list = ["0️⃣", "1️⃣", "2️⃣", "3️⃣"]

        if arg:
            emoji_list += ["4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]

        for emoji in emoji_list:
            await msg.add_reaction(emoji)

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


def setup(bot: discord.ext.commands.Bot):
    gst_bot.add_cog(DarkPoolShortsCommands(bot))
