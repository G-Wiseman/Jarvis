#!/usr/bin/env python3
import discord
from discord.ext import commands
import os
import re
import dotenv
from jarvis_image import jarvis_make_image
GUILD = discord.Object(id = int(dotenv.get_key(os.path("./.env"), "GUILD_ID")))

# New Discord.py 2.0.0 intents needed for Bot
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)
bot.name = "Jarvis"

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync(guild=GUILD)
    except Exception as e:
        print("Error syncing commands", e)

    print(f"{bot.name} Online")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
	await ctx.send("PONG")


@bot.tree.command(name="jarvis", guild=GUILD)
async def jarvis(interaction : discord.Interaction, message: str):
    path, name = jarvis_make_image(message)
    full_path = os.path.join(path,name)
    await interaction.response.send_message(f"OK {interaction.user.display_name}, can do", file=discord.File(full_path))
    try:
        os.remove(full_path)
        pass
    except Exception:
        pass


### Some Non Command Bot Functions
async def handle_mention(input_mention):
    """
    Takes the <@NUMBERS> generated with a mention, and
    returns a discord.user object. If the input string is not
    valid mentions, returns None.
    """
    regex = re.match("<@(.*)>", input_mention)

    user_id = regex.group(1)
    try:
        user = await bot.fetch_user(user_id)
    except  discord.NotFound as e:
        print(e)
        return None

    return user

#Now the bot's event loop should be run! It begins!
bot.run(dotenv.get_key(os.path("./.env"), "PRIVATE_KEY"))

