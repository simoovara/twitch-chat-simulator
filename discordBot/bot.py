import json
import discord
import re

from discord.ext import commands
from dotenv import dotenv_values
from websocket import create_connection, WebSocket

config = dotenv_values(".env")
FLARE_ID = 473216418851192853
SIMO_ID = 711625207361830912
bot = commands.Bot(command_prefix="flarege:", help_command=None, owner_ids=[FLARE_ID, SIMO_ID])

ws: WebSocket = create_connection("ws://localhost:8080")
@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")


def remove_pings(content):
    return re.sub("<@?\d+>", "", content).strip()

@bot.event
async def on_message(message):
    global ws
    if message.author.bot:
        return

    is_flare_mentioned = str(FLARE_ID) in message.content
    is_dm_channel = isinstance(message.channel, discord.DMChannel)

    if not is_flare_mentioned and not is_dm_channel:
        return

    content = remove_pings(message.content)

    data = {
        "type": "message",
        "messageContent": content,
        "author": message.author.name,
    }
    ws.send(json.dumps(data))

    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(config["TOKEN"])
