import discord
import matplotlib.pyplot as plt
import os
import datetime
import config_discordbot as cfg
from discordbot import gst_imgur

from gamestonk_terminal.economy import cnn_view, cnn_model


def feargreed_command():
    plt.ion()
    fig = plt.figure(figsize=[1, 1], dpi=10)

    report, _ = cnn_model.get_feargreed_report("", fig)
    cnn_view.fear_and_greed_index(indicator="", export="png")

    plt.close("all")

    now = datetime.datetime.now()
    image_path = os.path.join(
        cfg.GST_PATH,
        "exports",
        "economy",
        f"feargreed_{now.strftime('%Y%m%d_%H%M%S')}.png",
    )

    i = 0
    while not os.path.exists(image_path) and i < 10:
        now -= datetime.timedelta(seconds=1)
        image_path = os.path.join(
            cfg.GST_PATH,
            "exports",
            "economy",
            f"feargreed_{now.strftime('%Y%m%d_%H%M%S')}.png",
        )
        i += 1

    embed = discord.Embed(
        title="[CNN] Fear Geed Index", description=report, colour=cfg.COLOR
    )
    embed.set_author(
        name=cfg.AUTHOR_NAME,
        icon_url=cfg.AUTHOR_ICON_URL,
    )

    if os.path.exists(image_path):
        uploaded_image = gst_imgur.upload_image(image_path, title="FearGreed Charts")
        embed.set_image(url=uploaded_image.link)

    else:
        # report = "Error: The image could not be found"
        print("Error with uploading the the image to Imgur.")

    plt.close("all")
    return embed