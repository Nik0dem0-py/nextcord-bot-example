import nextcord
from nextcord.ext import commands
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class Utilities(commands.Cog):
    """
    Shows misc information
    """
    
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog "Ping" has been loaded')



    @commands.command()
    async def ping(self, ctx):
        logger.info("Ping command used")
        """Sends bot latency :ping_pong:"""
        await ctx.reply(f'Pong! :ping_pong: `{round(self.bot.latency * 1000)}ms`')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def setdelay(self, ctx, seconds: int):
        logger.info("Delay set to " + seconds + ctx.channel)
        """Sets slowmode in current channel"""
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.reply(f"Set the slowmode delay in this channel to {seconds} seconds!")

def setup(bot):
    bot.add_cog(Utilities(bot))