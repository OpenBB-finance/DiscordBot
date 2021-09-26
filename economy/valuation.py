import discord
import config_discordbot as cfg
from helpers import pagination

from gamestonk_terminal.economy import finviz_model

economy_group = {
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
}


async def valuation_command(ctx, arg="sector"):
    group = economy_group[arg]
    df_group = finviz_model.get_valuation_performance_data(group, "valuation")

    future_column_name = df_group["Name"]
    df_group = df_group.transpose()
    df_group.columns = future_column_name
    df_group.drop("Name")
    columns = []

    initial_str = "Page 0: Overview"
    i = 1
    for col_name in df_group.columns.values:
        initial_str += f"\nPage {i}: {col_name}"
        i += 1

    columns.append(
        discord.Embed(
            title=f"[Finviz] Valuation {group}",
            description=initial_str,
            colour=cfg.COLOR,
        ).set_author(
            name=cfg.AUTHOR_NAME,
            icon_url=cfg.AUTHOR_ICON_URL,
        )
    )
    for column in df_group.columns.values:
        columns.append(
            discord.Embed(
                description="```" + df_group[column].fillna("").to_string() + "```",
                colour=cfg.COLOR,
            ).set_author(
                name=cfg.AUTHOR_NAME,
                icon_url=cfg.AUTHOR_ICON_URL,
            )
        )

    await pagination(columns, ctx)
