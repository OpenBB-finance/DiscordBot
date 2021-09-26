from discord.ext import commands
import discord
from helpers import pagination
from discordbot import gst_bot
import config_discordbot as cfg
from stocks.stock_main import load
import os
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pyimgur

im = pyimgur.Imgur(cfg.IMGUR_CLIENT_ID)

from gamestonk_terminal.stocks.dark_pool_shorts import (
    yahoofinance_model,
    sec_model,
    finra_model,
    stockgrid_model,
    shortinterest_model,
)
from gamestonk_terminal.config_plot import PLOT_DPI


async def shorted_command(ctx, arg):
    arg = int(arg)
    df = yahoofinance_model.get_most_shorted().head(arg)
    df.dropna(how="all", axis=1, inplace=True)
    df = df.replace(float("NaN"), "")
    future_column_name = df["Symbol"]
    df = df.transpose()
    df.columns = future_column_name
    df.drop("Symbol")
    columns = []
    i = 2
    current = 0
    initial_str = "Page 1: Overview"
    for column in df.columns.values:
        initial_str = initial_str + "\nPage " + str(i) + ": " + column
        i += 1
    columns.append(
        discord.Embed(
            title="Most Shorted Stocks", description=initial_str, colour=cfg.COLOR
        ).set_author(
            name="Gamestonk Terminal",
            icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
        )
    )
    for column in df.columns.values:
        columns.append(
            discord.Embed(
                title="Most Shorted Stocks",
                description="```" + df[column].fillna("").to_string() + "```",
                colour=cfg.COLOR,
            ).set_author(
                name="Gamestonk Terminal",
                icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
            )
        )

    await pagination(columns, ctx)


def fail_to_deliver_command(ticker, start, end):
    if start == "":
        start = datetime.now() - timedelta(days=365)
    if end == "":
        end = datetime.now()
    if isinstance(start, str):
        start = datetime.strptime(start, cfg.DATE_FORMAT)
    if isinstance(end, str):
        end = datetime.strptime(end, cfg.DATE_FORMAT)
    plt.ion()
    ftds_data = sec_model.get_fails_to_deliver(ticker, start, end, 0)
    plt.bar(
        ftds_data["SETTLEMENT DATE"],
        ftds_data["QUANTITY (FAILS)"] / 1000,
    )
    plt.ylabel("Shares [K]")
    plt.title(f"Fails-to-deliver Data for {ticker}")
    plt.grid(b=True, which="major", color="#666666", linestyle="-", alpha=0.2)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
    plt.gcf().autofmt_xdate()
    plt.xlabel("Days")
    _ = plt.gca().twinx()
    stock = load(ticker, start)
    stock_ftd = stock[stock.index > start]
    stock_ftd = stock_ftd[stock_ftd.index < end]
    plt.plot(stock_ftd.index, stock_ftd["Adj Close"], color="tab:orange")
    plt.ylabel("Share Price [$]")
    plt.savefig("dps_ftd.png")
    plt.close("all")
    uploaded_image = im.upload_image("dps_ftd.png", title="something")
    image_link = uploaded_image.link
    title = "Fail to Deliever " + ticker
    embed = discord.Embed(title=title, colour=cfg.COLOR)
    embed.set_author(
        name="Gamestonk Terminal",
        icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
    )
    embed.set_image(url=image_link)
    os.remove("dps_ftd.png")
    return embed


def dark_pool_otc_command(ticker, start, end):
    if start == "":
        start = datetime.now() - timedelta(days=365)
    if end == "":
        end = datetime.now()
    if isinstance(start, str):
        start = datetime.strptime(start, cfg.DATE_FORMAT)
    if isinstance(end, str):
        end = datetime.strptime(end, cfg.DATE_FORMAT)
    plt.ion()

    title = "Dark Pool OTC " + ticker
    embed = discord.Embed(title=title, colour=cfg.COLOR)
    embed.set_author(
        name="Gamestonk Terminal",
        icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
    )
    ats, otc = finra_model.getTickerFINRAdata(ticker)

    if ats.empty and otc.empty:
        return embed.set_description("No data found.")
    _, _ = plt.subplots(dpi=PLOT_DPI)

    plt.subplot(3, 1, (1, 2))
    if not ats.empty and not otc.empty:
        plt.bar(
            ats.index,
            (ats["totalWeeklyShareQuantity"] + otc["totalWeeklyShareQuantity"])
            / 1_000_000,
            color="tab:orange",
        )
        plt.bar(
            otc.index, otc["totalWeeklyShareQuantity"] / 1_000_000, color="tab:blue"
        )
        plt.legend(["ATS", "OTC"])

    elif not ats.empty:
        plt.bar(
            ats.index,
            ats["totalWeeklyShareQuantity"] / 1_000_000,
            color="tab:orange",
        )
        plt.legend(["ATS"])

    elif not otc.empty:
        plt.bar(
            otc.index, otc["totalWeeklyShareQuantity"] / 1_000_000, color="tab:blue"
        )
        plt.legend(["OTC"])

    plt.ylabel("Total Weekly Shares [Million]")
    plt.grid(b=True, which="major", color="#666666", linestyle="-", alpha=0.2)
    plt.title(f"Dark Pools (ATS) vs OTC (Non-ATS) Data for {ticker}")

    plt.subplot(313)
    if not ats.empty:
        plt.plot(
            ats.index,
            ats["totalWeeklyShareQuantity"] / ats["totalWeeklyTradeCount"],
            color="tab:orange",
        )
        plt.legend(["ATS"])

        if not otc.empty:
            plt.plot(
                otc.index,
                otc["totalWeeklyShareQuantity"] / otc["totalWeeklyTradeCount"],
                color="tab:blue",
            )
            plt.legend(["ATS", "OTC"])

    else:
        plt.plot(
            otc.index,
            otc["totalWeeklyShareQuantity"] / otc["totalWeeklyTradeCount"],
            color="tab:blue",
        )
        plt.legend(["OTC"])

    plt.ylabel("Shares per Trade")
    plt.grid(b=True, which="major", color="#666666", linestyle="-", alpha=0.2)
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=4))
    plt.xlabel("Weeks")
    file_name = ticker + "_dpotc.png"
    plt.savefig(file_name)
    plt.close("all")
    uploaded_image = im.upload_image(file_name, title="something")
    image_link = uploaded_image.link
    embed.set_image(url=image_link)
    os.remove(file_name)

    return embed


def spos_command(ticker):
    plt.ion()
    title = "SPOS " + ticker
    embed = discord.Embed(title=title, colour=cfg.COLOR)
    embed.set_author(
        name="Gamestonk Terminal",
        icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
    )

    df = stockgrid_model.get_net_short_position(ticker)
    fig = plt.figure(dpi=PLOT_DPI)

    ax = fig.add_subplot(111)
    ax.bar(
        df["dates"],
        df["dollar_net_volume"] / 1_000,
        color="r",
        alpha=0.4,
        label="Net Short Vol. (1k $)",
    )
    ax.set_ylabel("Net Short Vol. (1k $)")

    ax2 = ax.twinx()
    ax2.plot(
        df["dates"].values,
        df["dollar_dp_position"],
        c="tab:blue",
        label="Position (1M $)",
    )
    ax2.set_ylabel("Position (1M $)")

    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc="upper left")

    ax.grid()
    plt.title(f"Net Short Vol. vs Position for {ticker}")
    plt.gcf().autofmt_xdate()
    file_name = ticker + "_spos.png"
    plt.savefig(file_name)
    plt.close("all")
    uploaded_image = im.upload_image(file_name, title="something")
    image_link = uploaded_image.link
    embed.set_image(url=image_link)
    os.remove(file_name)
    return embed


def psi_command(ticker):
    plt.ion()
    title = "PSI " + ticker
    embed = discord.Embed(title=title, colour=cfg.COLOR)
    embed.set_author(
        name="Gamestonk Terminal",
        icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
    )

    df, prices = stockgrid_model.get_short_interest_volume(ticker)

    _, axes = plt.subplots(
        2,
        1,
        dpi=PLOT_DPI,
        gridspec_kw={"height_ratios": [2, 1]},
    )

    axes[0].bar(
        df["date"],
        df["total_volume"] / 1_000_000,
        width=timedelta(days=1),
        color="b",
        alpha=0.4,
        label="Total Volume",
    )
    axes[0].bar(
        df["date"],
        df["short_volume"] / 1_000_000,
        width=timedelta(days=1),
        color="r",
        alpha=0.4,
        label="Short Volume",
    )

    axes[0].set_ylabel("Volume (1M)")
    ax2 = axes[0].twinx()
    ax2.plot(df["date"].values, prices[len(prices) - len(df) :], c="k", label="Price")
    ax2.set_ylabel("Price ($)")

    lines, labels = axes[0].get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc="upper left")

    axes[0].grid()
    axes[0].ticklabel_format(style="plain", axis="y")
    plt.title(f"Price vs Short Volume Interest for {ticker}")
    plt.gcf().autofmt_xdate()

    axes[1].plot(
        df["date"].values,
        100 * df["short_volume%"],
        c="green",
        label="Short Vol. %",
    )

    axes[1].set_ylabel("Short Vol. %")

    axes[1].grid(axis="y")
    lines, labels = axes[1].get_legend_handles_labels()
    axes[1].legend(lines, labels, loc="upper left")
    axes[1].set_ylim([0, 100])
    file_name = ticker + "_psi.png"
    plt.savefig(file_name)
    plt.close("all")
    uploaded_image = im.upload_image(file_name, title="something")
    image_link = uploaded_image.link
    embed.set_image(url=image_link)
    os.remove(file_name)

    return embed


async def high_short_interest_command(ctx, num):
    df = shortinterest_model.get_high_short_interest()
    df = df.iloc[1:].head(n=num)

    future_column_name = df["Ticker"]
    df = df.transpose()
    df.columns = future_column_name
    df.drop("Ticker")
    columns = []
    i = 2
    current = 0
    initial_str = "Page 1: Overview"
    for column in df.columns.values:
        initial_str = initial_str + "\nPage " + str(i) + ": " + column
        i += 1
    columns.append(
        discord.Embed(
            title="High Short Interest", description=initial_str, colour=cfg.COLOR
        ).set_author(
            name="Gamestonk Terminal",
            icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
        )
    )
    for column in df.columns.values:
        columns.append(
            discord.Embed(
                title="High Short Interest",
                description="```" + df[column].fillna("").to_string() + "```",
                colour=cfg.COLOR,
            ).set_author(
                name="Gamestonk Terminal",
                icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
            )
        )

    await pagination(columns, ctx)


async def pos_command(ctx, num, sort):
    df = stockgrid_model.get_dark_pool_short_positions(sort, False)
    df = df.iloc[:num]
    dp_date = df["Date"].values[0]
    df = df.drop(columns=["Date"])
    df["Net Short Volume $"] = df["Net Short Volume $"] / 100_000_000
    df["Short Volume"] = df["Short Volume"] / 1_000_000
    df["Net Short Volume"] = df["Net Short Volume"] / 1_000_000
    df["Short Volume %"] = df["Short Volume %"] * 100
    df["Dark Pools Position $"] = df["Dark Pools Position $"] / (1_000_000_000)
    df["Dark Pools Position"] = df["Dark Pools Position"] / 1_000_000
    df.columns = [
        "Ticker",
        "Short Vol. (1M)",
        "Short Vol. %",
        "Net Short Vol. (1M)",
        "Net Short Vol. ($100M)",
        "DP Position (1M)",
        "DP Position ($1B)",
    ]
    future_column_name = df["Ticker"]
    df = df.transpose()
    df.columns = future_column_name
    df.drop("Ticker")
    columns = []
    i = 2
    current = 0
    initial_str = "Page 1: Overview"
    for column in df.columns.values:
        initial_str = initial_str + "\nPage " + str(i) + ": " + column
        i += 1
    columns.append(
        discord.Embed(
            title="Dark Pool Short Position", description=initial_str, colour=cfg.COLOR
        ).set_author(
            name="Gamestonk Terminal",
            icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
        )
    )
    for column in df.columns.values:
        columns.append(
            discord.Embed(
                title="High Short Interest",
                description="```The following data corresponds to the date: "
                + dp_date
                + "\n\n"
                + df[column].fillna("").to_string()
                + "```",
                colour=cfg.COLOR,
            ).set_author(
                name="Gamestonk Terminal",
                icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
            )
        )

    await pagination(columns, ctx)


async def sidtc_command(ctx, num, sort):
    df = stockgrid_model.get_short_interest_days_to_cover(sort)
    df = df.iloc[:num]
    dp_date = df["Date"].values[0]
    df = df.drop(columns=["Date"])
    df["Short Interest"] = df["Short Interest"] / 1_000_000
    df.head()
    df.columns = [
        "Ticker",
        "Float Short %",
        "Days to Cover",
        "Short Interest (1M)",
    ]
    future_column_name = df["Ticker"]
    df = df.transpose()
    df.columns = future_column_name
    df.drop("Ticker")
    columns = []
    i = 2
    current = 0
    initial_str = "Page 1: Overview"
    for column in df.columns.values:
        initial_str = initial_str + "\nPage " + str(i) + ": " + column
        i += 1
    columns.append(
        discord.Embed(
            title="Dark Pool Shorts", description=initial_str, colour=cfg.COLOR
        ).set_author(
            name="Gamestonk Terminal",
            icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
        )
    )
    for column in df.columns.values:
        columns.append(
            discord.Embed(
                title="High Short Interest",
                description="```The following data corresponds to the date: "
                + dp_date
                + "\n\n"
                + df[column].fillna("").to_string()
                + "```",
                colour=cfg.COLOR,
            ).set_author(
                name="Gamestonk Terminal",
                icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
            )
        )

    await pagination(columns, ctx)


class DarkPoolShortsCommands(commands.Cog):
    """A couple of simple commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="stocks.dps.shorted")
    async def shorted(self, ctx: commands.Context, arg="5"):
        arg = int(arg)
        await shorted_command(ctx, arg)

    @commands.command(name="stocks.dps.ftd")
    async def fail_to_deliver(self, ctx: commands.Context, arg, arg2="", arg3=""):
        embed = fail_to_deliver_command(arg, arg2, arg3)
        await ctx.send(embed=embed)

    @commands.command(name="stocks.dps.dpotc")
    async def dark_pool_otc(self, ctx: commands.Context, arg, arg2="", arg3=""):
        embed = dark_pool_otc_command(arg, arg2, arg3)
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
    async def high_short_interest(self, ctx: commands.Context, arg="10"):
        arg = int(arg)
        await high_short_interest_command(ctx, arg)

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
            + +")\n\n4️⃣"
            "!stocks.dps.ftd TICKER DATE_START DATE_END\n\n5️⃣ !stocks.dps.dpotc TICKER DATE_START DATE_END\n\n6️⃣ "
            "!stocks.dps.spos TICKER\n\n7️⃣ !stocks.dps.psi TICKER"
        )

        title = "Dark Pool Shorts (DPS) Menu"
        embed = discord.Embed(title=title, description=text, colour=cfg.COLOR)
        embed.set_author(
            name="Gamestonk Terminal",
            icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
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
                await high_short_interest_command(ctx, 10)
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
