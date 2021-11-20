import nextcord
from nextcord.ext import commands

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
        """Sends bot latency :ping_pong:"""
        await ctx.send(f'Pong! :ping_pong: `{round(self.bot.latency * 1000)}ms`')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def setdelay(self, ctx, seconds: int):
        """Sets slowmode in current channel"""
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

def setup(bot):
    bot.add_cog(Utilities(bot))