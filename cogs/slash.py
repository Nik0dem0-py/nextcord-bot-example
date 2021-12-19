from nextcord.ext import commands
from discord_ui import UI
from discord_ui.cogs import slash_command, subslash_command, listening_component
import config



class Example(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="test", guild_ids=config.GUILD_IDS)
    async def test(self, ctx):
        await ctx.respond("test")


def setup(bot):
	bot.add_cog(Example(bot))