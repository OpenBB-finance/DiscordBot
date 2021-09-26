import discord
import asyncio
import config_discordbot as cfg
from discordbot import gst_bot

from economy.feargreed import feargreed_command
from economy.overview import overview_command
from economy.indices import indices_command
from economy.futures import futures_command
from economy.usbonds import usbonds_command
from economy.glbonds import glbonds_command
from economy.currencies import currencies_command
from economy.valuation import valuation_command
from economy.performance import performance_command


class EconomyCommands(discord.ext.commands.Cog):
    """Economy Commands menu"""

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @discord.ext.commands.command(name="economy.feargreed")
    async def feargreed(self, ctx: discord.ext.commands.Context):
        embed = feargreed_command()
        await ctx.send(embed=embed)

    @discord.ext.commands.command(name="economy.overview")
    async def overview(self, ctx: discord.ext.commands.Context):
        embed = overview_command()
        await ctx.send(embed=embed)

    @discord.ext.commands.command(name="economy.indices")
    async def indices(self, ctx: discord.ext.commands.Context):
        embed = indices_command()
        await ctx.send(embed=embed)

    @discord.ext.commands.command(name="economy.futures")
    async def futures(self, ctx: discord.ext.commands.Context):
        embed = futures_command()
        await ctx.send(embed=embed)

    @discord.ext.commands.command(name="economy.usbonds")
    async def usbonds(self, ctx: discord.ext.commands.Context):
        embed = usbonds_command()
        await ctx.send(embed=embed)

    @discord.ext.commands.command(name="economy.glbonds")
    async def glbonds(self, ctx: discord.ext.commands.Context):
        embed = glbonds_command()
        await ctx.send(embed=embed)

    @discord.ext.commands.command(name="economy.currencies")
    async def currencies(self, ctx: discord.ext.commands.Context):
        embed = currencies_command()
        await ctx.send(embed=embed)

    @discord.ext.commands.command(name="economy.valuation")
    async def valuation(self, ctx: discord.ext.commands.Context, arg=""):
        if arg:
            await valuation_command(ctx, arg)
        else:
            await valuation_command(ctx)

    @discord.ext.commands.command(name="economy.performance")
    async def performance(self, ctx: discord.ext.commands.Context, arg=""):
        if arg:
            await performance_command(ctx, arg)
        else:
            await performance_command(ctx)

    @discord.ext.commands.command(name="economy")
    async def economy(self, ctx: discord.ext.commands.Context):
        text = (
            "0️⃣ !economy.overview\n"
            "1️⃣ !economy.futures\n"
            "2️⃣ !economy.usbonds\n"
            "3️⃣ !economy.glbonds\n"
            "4️⃣ !economy.indices\n"
            "5️⃣ !economy.currencies\n"
            "6️⃣ !economy.feargreed\n"
            "7️⃣ !economy.valuation <GROUP> (default: sector)\n"
            "8️⃣ !economy.performance <GROUP> (default: sector)"
        )

        title = "Economy Menu"
        embed = discord.Embed(title=title, description=text, colour=cfg.COLOR)
        embed.set_author(
            name="Gamestonk Terminal",
            icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
        )
        msg = await ctx.send(embed=embed)

        emoji_list = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]

        for emoji in emoji_list:
            await msg.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in emoji_list

        try:
            reaction, user = await gst_bot.wait_for(
                "reaction_add", timeout=10, check=check
            )
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
                await valuation_command(ctx)
            elif reaction.emoji == "8️⃣":
                await performance_command(ctx, "")

            await msg.remove_reaction(reaction.emoji, user)

            # TODO: Make this work - may need to set different discord server configurations
            # for emoji in emoji_list:
            #    await msg.remove_reaction(emoji, user)

        except asyncio.TimeoutError:
            text = text + "\n\nCOMMAND TIMEOUT."
            embed = discord.Embed(title=title, description=text)
            await msg.edit(embed=embed)


def setup(bot: discord.ext.commands.Bot):
    gst_bot.add_cog(EconomyCommands(bot))
