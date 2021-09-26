import sys
import discord
import discord_components
import asyncio
import config_discordbot as cfg

# Sets the prefix to the commands
activity = discord.Game(
    name="Gametonk Terminal: https://github.com/GamestonkTerminal/GamestonkTerminal"
)
date_input_format = "%Y-%m-%d"  # Enter your prefered date input format

## Defining the bot ##
gst_bot = discord.ext.commands.Bot(
    command_prefix=cfg.COMMAND_PREFIX, intents=discord.Intents.all(), activity=activity
)
discord_components.DiscordComponents(gst_bot)

bot_colour = discord.Color.from_rgb(0, 206, 154)


async def pagination(dataset_with_embeds, ctx):
    current = 0
    components = [
        [
            discord_components.Button(
                label="Prev", id="back", style=discord_components.ButtonStyle.red
            ),
            discord_components.Button(
                label=f"Page {int(dataset_with_embeds.index(dataset_with_embeds[current]))}/{len(dataset_with_embeds)}",
                id="cur",
                style=discord_components.ButtonStyle.green,
                disabled=True,
            ),
            discord_components.Button(
                label="Next", id="front", style=discord_components.ButtonStyle.green
            ),
        ]
    ]
    mainMessage = await ctx.send(
        embed=dataset_with_embeds[current], components=components
    )
    while True:
        # Try and except blocks to catch timeout and break
        try:
            interaction = await gst_bot.wait_for(
                "button_click",
                check=lambda i: i.component.id in ["back", "front"],  # You can add more
                timeout=30.0,  # 30 seconds of inactivity
            )
            # Getting the right list index
            if interaction.component.id == "back":
                current -= 1
            elif interaction.component.id == "front":
                current += 1
            # If its out of index, go back to start / end
            if current == len(dataset_with_embeds):
                current = 0
            elif current < 0:
                current = len(dataset_with_embeds) - 1

            # Edit to new page + the center counter changes
            components = [
                [
                    discord_components.Button(
                        label="Prev",
                        id="back",
                        style=discord_components.ButtonStyle.red,
                    ),
                    discord_components.Button(
                        label=f"Page {int(dataset_with_embeds.index(dataset_with_embeds[current]))}/{len(dataset_with_embeds)}",
                        id="cur",
                        style=discord_components.ButtonStyle.green,
                        disabled=True,
                    ),
                    discord_components.Button(
                        label="Next",
                        id="front",
                        style=discord_components.ButtonStyle.green,
                    ),
                ]
            ]

            await interaction.edit_origin(
                embed=dataset_with_embeds[current], components=components
            )
        except asyncio.TimeoutError:
            # Disable and get outta here
            components = [
                [
                    discord_components.Button(
                        label="Prev",
                        id="back",
                        style=discord_components.ButtonStyle.green,
                        disabled=True,
                    ),
                    discord_components.Button(
                        label=f"Page {int(dataset_with_embeds.index(dataset_with_embeds[current])) + 1}/{len(dataset_with_embeds)}",
                        id="cur",
                        style=discord_components.ButtonStyle.grey,
                        disabled=True,
                    ),
                    discord_components.Button(
                        label="Next",
                        id="front",
                        style=discord_components.ButtonStyle.green,
                        disabled=True,
                    ),
                ]
            ]
            await mainMessage.edit(components=components)
            break


async def on_ready():
    print("Bot Online")


## Loads the commands (Cogs) from each "context" ##
gst_bot.load_extension("general_commands")
gst_bot.load_extension("economy_commands")
gst_bot.load_extension("stocks.dark_pool_shorts")

## Runs the bot ##
gst_bot.run(cfg.DISCORD_BOT_TOKEN)
