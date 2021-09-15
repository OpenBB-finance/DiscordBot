from discord.ext import commands
import discord
from main import bot_colour


class GeneralCommands(commands.Cog):
    """A couple of simple commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="about")
    async def hello_world(self, ctx: commands.Context):
        links = (
            "Join our community on discord: https://discord.gg/Up2QGbMKHY\n"
            "Follow our twitter for updates: https://twitter.com/gamestonkt\n"
            "Access our landing page: https://gamestonkterminal.vercel.app\n\n"
            "**Maintainers:** DidierRLopes, jmaslek, aia\n"
        )
        partnerships = (
            "FinBrain: https://finbrain.tech\n"
            "Quiver Quantitative: https://www.quiverquant.com\n"
            "Ops.Syncretism: https://ops.syncretism.io/api.html\n"
            "SentimentInvestor: https://sentimentinvestor.com\n"
            "The Geek of Wall Street: https://thegeekofwallstreet.com\n"
        )
        disclaimer = "Trading in financial instruments involves high risks including the risk of losing some, or all, of your investment amount, and may not be suitable for all investors. Before deciding to trade in financial instrument you should be fully informed of the risks and costs associated with trading the financial markets, carefully consider your investment objectives, level of experience, and risk appetite, and seek professional advice where needed. The data contained in Gamestonk Terminal (GST) is not necessarily accurate. GST and any provider of the data contained in this website will not accept liability for any loss or damage as a result of your trading, or your reliance on the information displayed."

        embed = discord.Embed(
            title="Investment Research for Everyone",
            description=links,
            colour=bot_colour,
        )
        embed.set_author(
            name="Gamestonk Terminal",
            icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
        )
        embed.add_field(name="Partnerships:", value=partnerships, inline=False)
        embed.add_field(name="Disclaimer:", value=disclaimer, inline=False)

        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(GeneralCommands(bot))
