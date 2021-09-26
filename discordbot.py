import discord
import discord_components
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


async def on_ready():
    print("Bot Online")


## Loads the commands (Cogs) from each "context" ##
gst_bot.load_extension("general_commands")
gst_bot.load_extension("economy_commands")
gst_bot.load_extension("stocks.dark_pool_shorts")

## Runs the bot ##
gst_bot.run(cfg.DISCORD_BOT_TOKEN)
