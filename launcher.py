from nextcord import Client, Intents, Embed, guild
import nextcord 
from nextcord.ext import commands, tasks
import os
from nextcord.ext.commands.core import has_permissions, MissingPermissions
from dotenv import load_dotenv
import asyncio
from nextcord.ext.tasks import loop
from asyncio import sleep
import random
from itertools import cycle
import config
import sys






bot = commands.Bot(command_prefix=config.PREFIX, case_insensitive=True)
bot.remove_command('help')




@tasks.loop(seconds=10.0)
@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Game(name="I'm a bot"))






@bot.event
async def on_ready():
    print("Bot is online.")





@bot.command
@commands.has_permissions(manage_channels=True)
async def load(ctx, extension):
    if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded Cog `{extension}`.')  



@bot.command()
@commands.has_permissions(manage_channels=True)
async def unload(ctx, extension):
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded Cog `{extension}`.')

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


load_dotenv()

TOKEN = os.getenv("bottoken")



bot.run(TOKEN, reconnect=True)


