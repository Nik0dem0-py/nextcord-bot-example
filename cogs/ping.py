import discord
from discord.ext import commands

class Ping(commands.Cog):
    
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog "Ping" has been loaded')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! `{round(self.bot.latency * 1000)}ms`')

def setup(bot):
    bot.add_cog(Ping(bot))