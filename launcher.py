from discord import Client, Intents, Embed, guild
import discord
from discord.ext import commands, tasks
import os
from discord_slash.utils.manage_commands import create_option, create_choice
from dotenv import load_dotenv
from discord_slash import SlashCommand
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils import manage_components
import asyncio
from discord.ext.tasks import loop
from asyncio import sleep
import random
from itertools import cycle






bot = commands.Bot(command_prefix=".", case_insensitive=True)
bot.remove_command('help')






@tasks.loop(minutes=1.0)
async def status_task():
    statuses = ["I'm on Nik0dem0-py's Github!", "Hello there! ", "This bot is still getting developed!"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))



@bot.event
async def on_ready():
    print("Bot is online.")


@bot.command()
async def load(ctx, extension):
    if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
        bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
        bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


load_dotenv()

TOKEN = os.getenv("bottoken")
bot.run(TOKEN)


