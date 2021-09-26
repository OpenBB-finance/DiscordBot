import discord
import config_discordbot as cfg
from helpers import pagination

from gamestonk_terminal.stocks.dark_pool_shorts import yahoofinance_model


async def shorted_command(ctx, arg="5"):
    df = yahoofinance_model.get_most_shorted().head(int(arg))

    df.dropna(how="all", axis=1, inplace=True)
    df = df.replace(float("NaN"), "")
    future_column_name = df["Symbol"]
    df = df.transpose()
    df.columns = future_column_name
    df.drop("Symbol")
    columns = []

    initial_str = "Page 0: Overview"
    i = 1

    for col_name in df.columns.values:
        initial_str += f"\nPage {i}: {col_name}"
        i += 1

    columns.append(
        discord.Embed(
            title="[Yahoo Finance] Most Shorted Stocks",
            description=initial_str,
            colour=cfg.COLOR,
        ).set_author(
            name=cfg.AUTHOR_NAME,
            icon_url=cfg.AUTHOR_ICON_URL,
        )
    )
    for column in df.columns.values:
        columns.append(
            discord.Embed(
                description="```" + df[column].fillna("").to_string() + "```",
                colour=cfg.COLOR,
            ).set_author(
                name=cfg.AUTHOR_NAME,
                icon_url=cfg.AUTHOR_ICON_URL,
            )
        )

    await pagination(columns, ctx)
