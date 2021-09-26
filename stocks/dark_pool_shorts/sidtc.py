import discord
import config_discordbot as cfg
from helpers import pagination

from gamestonk_terminal.stocks.dark_pool_shorts import stockgrid_model


async def sidtc_command(ctx, arg, arg2):
    # Select default
    if not arg:
        arg = "10"
    if not arg2:
        arg2 = "float"

    # Help
    if arg == "-h":
        dark_pool_sort = {
            "float": "Float Short %",
            "dtc": "Days to Cover",
            "si": "Short Interest",
        }

        help_txt = "Get short interest and days to cover. [Source: Stockgrid]\n"

        possible_args = ""
        for k, v in dark_pool_sort.items():
            possible_args += f"\n{k}: {v}"

        help_txt += "\nPossible argments:\n"
        help_txt += "<NUM> Number of top tickers to show. Default: 10\n"
        help_txt += "<SORT> Field for which to sort by. Default: float\n"
        help_txt += f"The choices are:{possible_args}"

        embed = discord.Embed(
            title="Stocks: [Stockgrid] Short Interest and Days to Cover HELP",
            description=help_txt,
            colour=cfg.COLOR,
        )
        embed.set_author(
            name=cfg.AUTHOR_NAME,
            icon_url=cfg.AUTHOR_ICON_URL,
        )

        await ctx.send(embed=embed)

    else:
        # Parse argument
        num = int(arg)
        sort = arg2

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
        initial_str = "Page 0: Overview"
        i = 1
        for column in df.columns.values:
            initial_str = initial_str + "\nPage " + str(i) + ": " + column
            i += 1
        columns.append(
            discord.Embed(
                title="Dark Pool Shorts", description=initial_str, colour=cfg.COLOR
            ).set_author(
                name=cfg.AUTHOR_NAME,
                icon_url=cfg.AUTHOR_ICON_URL,
            )
        )
        for column in df.columns.values:
            columns.append(
                discord.Embed(
                    title="Stocks: [Stockgrid] Short Interest and Days to Cover",
                    description="```The following data corresponds to the date: "
                    + dp_date
                    + "\n\n"
                    + df[column].fillna("").to_string()
                    + "```",
                    colour=cfg.COLOR,
                ).set_author(
                    name=cfg.AUTHOR_NAME,
                    icon_url=cfg.AUTHOR_ICON_URL,
                )
            )

        await pagination(columns, ctx)
