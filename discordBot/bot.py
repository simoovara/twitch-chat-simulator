import json
import discord
import re
import asyncio

from discord.ext import commands
from dotenv import dotenv_values
from websocket import create_connection, WebSocket
from pynput.keyboard import Key, Controller, KeyCode
from obs_websocket_client import OBSWebsocket

keyboard = Controller()
# for some reason pynput doesnt have these defined
f21 = KeyCode.from_vk(0x84)
f22 = KeyCode.from_vk(0x85)
f23 = KeyCode.from_vk(0x86)
f24 = KeyCode.from_vk(0x87)

config = dotenv_values(".env")
FLARE_ID = 473216418851192853
SIMO_ID = 711625207361830912
bot = commands.Bot(command_prefix="flarege:", help_command=None, owner_ids=[FLARE_ID, SIMO_ID])

model_lock = False
model_unlock_task = None
model_toggles = {
    "!on": Key.f13,
    "!off": Key.f14,
    "!xdx": Key.f15,
    "!hands": Key.f16,
    "!default": Key.f17,
    "!small": Key.f18,
    "!spin": Key.f19,
    "!guh": Key.f20,
    "!bread": f21,
    "!boop": f22
}


ws: WebSocket = create_connection("ws://localhost:8080")
obs_ws = OBSWebsocket(config["OBS_WS_IP"], 4455)
@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")


def remove_pings(content):
    return re.sub(r"<@?\d+>", "", content).strip()


def remove_discord_emojis(content):
    content = re.sub(r"\[.+\]\(.+\)", "", content).strip()  # removes FakeNitro emojis (and every other hyperlink but oh well)
    content = re.sub(r"<a?:", "", content).strip()
    return re.sub(r":\d+>", "", content).strip()


def check_for_commands(content):
    cmds = list(model_toggles.keys())
    try:
        return [cmd for cmd in cmds if cmd in content][0]  # only one command can be run at a time
    except IndexError:
        return None


def check_for_blacklisted(author_id):
    with open("blacklist.txt", "r") as file:
        return author_id in file.readlines()


async def unlock_model():
    global model_lock
    obs_ws.send_start_timer()
    await asyncio.sleep(15 * 60)  # 15 minutes in seconds
    model_lock = False
    obs_ws.send_reset_timer()


@bot.event
async def on_message(message):
    global ws, model_lock, model_unlock_task
    is_highlight = False
    if message.author == bot.user:
        return

    is_flare_mentioned = str(FLARE_ID) in message.content
    is_dm_channel = isinstance(message.channel, discord.DMChannel)
    is_vcathon_channel = message.channel.id == 1332431502918549515

    if not is_vcathon_channel and not is_dm_channel:
        return

    if message.author.id == 1332511728323526686:  # whisper message
        # scuffed but i dont wanna use regex
        if "by <@473216418851192853>" in message.content:
           if "model lock (15 mins)" in message.content:
               model_lock = True
               if model_unlock_task and not model_unlock_task.done():
                   obs_ws.send_pause_timer()
                   obs_ws.send_reset_timer()
                   model_unlock_task.cancel()

               model_unlock_task = asyncio.create_task(unlock_model)



    if is_flare_mentioned or is_dm_channel:
        is_highlight = True

    if check_for_blacklisted(message.author.id):
        return

    content = remove_pings(message.content)
    content = remove_discord_emojis(content)
    toggle = check_for_commands(content)
    if toggle and is_flare_mentioned and not model_lock:
        keyboard.press(model_toggles[toggle])
        keyboard.release(model_toggles[toggle])

    data = {
        "type": "message",
        "messageContent": content,
        "author": message.author.display_name if not is_dm_channel else None,
        "highlight": is_highlight,
    }
    ws.send(json.dumps(data))

    await bot.process_commands(message)


if __name__ == "__main__":
    bot.run(config["TOKEN"])
