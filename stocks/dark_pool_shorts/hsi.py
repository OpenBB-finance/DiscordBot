import discord
import config_discordbot as cfg
from helpers import pagination

from gamestonk_terminal.stocks.dark_pool_shorts import shortinterest_model


async def hsi_command(ctx, num):
    df = shortinterest_model.get_high_short_interest()
    df = df.iloc[1:].head(n=num)

    future_column_name = df["Ticker"]
    df = df.transpose()
    df.columns = future_column_name
    df.drop("Ticker")
    columns = []
    initial_str = "Page 0: Overview"
    i = 1
    for column in df.columns.values:
        initial_str = initial_str + "\nPage " + str(i) + ": " + column
        i += 1
    columns.append(
        discord.Embed(
            title="High Short Interest", description=initial_str, colour=cfg.COLOR
        ).set_author(
            name=cfg.AUTHOR_NAME,
            icon_url=cfg.AUTHOR_ICON_URL,
        )
    )
    for column in df.columns.values:
        columns.append(
            discord.Embed(
                title="High Short Interest",
                description="```" + df[column].fillna("").to_string() + "```",
                colour=cfg.COLOR,
            ).set_author(
                name=cfg.AUTHOR_NAME,
                icon_url=cfg.AUTHOR_ICON_URL,
            )
        )

    await pagination(columns, ctx)