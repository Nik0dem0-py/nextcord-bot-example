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
        print('Cog "Calculator 🧮" has been loaded.')
    

    @commands.command()
    async def add(self, ctx, *nums):
        """Adds two numbers."""
        var = f' {"+"} '.join(nums)
        await ctx.send(f"||{var}|| = **`{eval(var)}`** 🧮")

    @commands.command()
    async def multiply(self, ctx, *nums):
        """Multiplies two numbers."""
        var = f' {"*"} '.join(nums)
        await ctx.send(f"||{var}|| = **`{eval(var)}`** 🧮")
    
    @commands.command()
    async def divide(self, ctx, *nums):
        """Divides two number."""
        var = f' {"/"} '.join(nums)
        await ctx.send(f"||{var}|| = **`{eval(var)}`** 🧮")
    
    @commands.command()
    async def subtract(self, ctx, *nums):
        """Subtracts two numbers."""
        var = f' {"-"} '.join(nums)
        await ctx.send(f"||{var}|| = **`{eval(var)}`** 🧮")


def setup(bot):
    bot.add_cog(Calculator(bot))