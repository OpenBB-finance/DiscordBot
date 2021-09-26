import discord
import config_discordbot as cfg

from gamestonk_terminal.economy import wsj_model


def currencies_command():
    df_data = wsj_model.global_currencies()
    if df_data.empty:
        df_data_str = "No currencies data available"
    else:
        df_data_str = "```" + df_data.to_string(index=False) + "```"

    embed = discord.Embed(
        title="[WSJ] Currencies", description=df_data_str, colour=cfg.COLOR
    )
    embed.set_author(
        name="Gamestonk Terminal",
        icon_url="https://github.com/GamestonkTerminal/GamestonkTerminal/blob/main/images/gst_logo_rGreen.png?raw=true",
    )

    return embed
