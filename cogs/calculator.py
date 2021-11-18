import nextcord
from nextcord.ext import commands

class Calculator(commands.Cog):
    """
    All calculation commands
    """
    
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog "Calculator" has been loaded.')
    

    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers."""
        await ctx.send(left + right)

    @commands.command()
    async def multiply(self, ctx, left: int, right: int):
        """Multiplies two numbers."""
        await ctx.send(left * right)
    
    @commands.command()
    async def divide(self, ctx, left: int, right: int):
        """Divides two number."""
        await ctx.send(left / right)
    
    @commands.command()
    async def subtract(self, ctx, left: int, right: int):
        """Subtracts two numbers."""
        await ctx.send(left - right)


def setup(bot):
    bot.add_cog(Calculator(bot))