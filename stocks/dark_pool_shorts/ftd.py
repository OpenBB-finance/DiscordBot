import discord
import config_discordbot as cfg
from discordbot import gst_imgur
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import os
import helpers

from gamestonk_terminal.stocks.dark_pool_shorts import sec_model


def ftd_command(ticker, start, end):
    if start == "":
        start = datetime.now() - timedelta(days=365)
    else:
        start = datetime.strptime(start, cfg.DATE_FORMAT)

    if end == "":
        end = datetime.now()
    else:
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
    stock = helpers.load(ticker, start)
    stock_ftd = stock[stock.index > start]
    stock_ftd = stock_ftd[stock_ftd.index < end]
    plt.plot(stock_ftd.index, stock_ftd["Adj Close"], color="tab:orange")
    plt.ylabel("Share Price [$]")
    plt.savefig("dps_ftd.png")
    plt.close("all")
    uploaded_image = gst_imgur.upload_image("dps_ftd.png", title="something")
    image_link = uploaded_image.link
    title = "Fail to Deliever " + ticker
    embed = discord.Embed(title=title, colour=cfg.COLOR)
    embed.set_author(
        name=cfg.AUTHOR_NAME,
        icon_url=cfg.AUTHOR_ICON_URL,
    )
    embed.set_image(url=image_link)
    os.remove("dps_ftd.png")
    return embed