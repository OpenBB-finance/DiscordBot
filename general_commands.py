from discord.ext import commands
import discord

class GeneralCommands(commands.Cog):
    """A couple of simple commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="about")
    async def hello_world(self, ctx: commands.Context):
        text_main =    "Join our community on discord: https://discord.gg/Up2QGbMKHY\n" \
                       "Follow our twitter for updates: https://twitter.com/gamestonkt\n" \
                       "Access our landing page: https://gamestonkterminal.vercel.app\n\n" \
                       "Author: DidierRLopes\n" \
                       "Main Devs: jmaslek, aia\n"

        field_value_1 = "Working towards a GUI using Qt: piiq, hinxx\n" \
                        "Working on our landing page: jose-donato, crspy, martiaaz\n" \
                        "Managing Twitter account: Meghan Honen\n" \
                        "Responsible by developing Forex menu: alokan\n" \
                        "Degiro's integration: Chavithra, Deel18\n" \
                        "Preset screeners: Traceabl3\n" \

        field_value_2 = "FinBrain: https://finbrain.tech\n" \
                        "Quiver Quantitative: https://www.quiverquant.com\n" \
                        "Ops.Syncretism: https://ops.syncretism.io/api.html\n" \
                        "SentimentInvestor: https://sentimentinvestor.com\n" \
                        "The Geek of Wall Street: https://thegeekofwallstreet.com\n" \

        field_value_3 = "Use the prefix + disclaimer (ex. !disclaimer) for more information"

        embed = discord.Embed(title="Thanks for using Gamestonk Terminal. This is our way!", description=text_main,
                              colour=discord.Color.from_rgb(0, 206, 154))
        embed.set_author(name="Gamestonk Terminal",
                         icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true")
        embed.add_field(name="Main Contributors:", value= field_value_1, inline=False)
        embed.add_field(name="Partnerships:", value=field_value_2, inline=False)
        embed.add_field(name="DISCLAIMER:", value=field_value_3, inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="disclaimer")
    async def disclaimer(self, ctx: commands.Context):
        text_main = "Trading in financial instruments involves high risks including the risk of losing some, or all, of your investment amount, and may not be suitable for all investors. Before deciding to trade in financial instrument you should be fully informed of the risks and costs associated with trading the financial markets, carefully consider your investment objectives, level of experience, and risk appetite, and seek professional advice where needed. The data contained in Gamestonk Terminal (GST) is not necessarily accurate. GST and any provider of the data contained in this website will not accept liability for any loss or damage as a result of your trading, or your reliance on the information displayed."
        embed = discord.Embed(title="DISCLAIMER:", description=text_main, colour=discord.Color.from_rgb(0, 206, 154))
        embed.set_author(name="Gamestonk Terminal",
                         icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true")
        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(GeneralCommands(bot))
