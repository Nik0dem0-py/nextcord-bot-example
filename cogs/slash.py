from nextcord.ext import commands
from discord_ui import UI
from discord_ui.cogs import slash_command, subslash_command, listening_component




class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="example", guild_ids=[811178517969895474])
    async def example(self, ctx):
        await ctx.respond("gotchu", hidden=True)


def setup(bot):
	bot.add_cog(Example(bot))