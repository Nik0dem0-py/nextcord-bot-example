import nextcord
from nextcord.ext import commands
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class Calculator(commands.Cog):
    """
    All calculation commands
    """
    
    
    def __init__(self, bot):
        self.bot = bot
    
    

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog "Calculator 🧮" has been loaded.')
    

    @commands.command()
    async def add(self, ctx, *nums):
        """Adds two numbers."""
        var = f' {"+"} '.join(nums)
        await ctx.reply(f"||{var}|| = **`{eval(var)}`** 🧮")

    @commands.command()
    async def multiply(self, ctx, *nums):
        """Multiplies two numbers."""
        var = f' {"*"} '.join(nums)
        await ctx.reply(f"||{var}|| = **`{eval(var)}`** 🧮")
    
    @commands.command()
    async def divide(self, ctx, *nums):
        """Divides two numbers."""
        var = f' {"/"} '.join(nums)
        await ctx.reply(f"||{var}|| = **`{eval(var)}`** 🧮")
    
    @commands.command()
    async def subtract(self, ctx, *nums):
        """Subtracts two numbers."""
        var = f' {"-"} '.join(nums)
        await ctx.reply(f"||{var}|| = **`{eval(var)}`** 🧮")
    

    


def setup(bot):
    bot.add_cog(Calculator(bot))