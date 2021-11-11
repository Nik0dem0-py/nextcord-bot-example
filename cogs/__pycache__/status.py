import discord
from discord.ext import commands, tasks
from itertools import cycle

from discord.ext.commands import bot
class Status(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.status = cycle(["Test 1", "Test 2", "Test 3"]) 
        self.change_status.start() 

    
    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start() 
        print("Changing Status")
        await self.client.change_presence(activity = discord.Game(next(self.status)))

def setup(bot):
    bot.add_cog(Status(bot))