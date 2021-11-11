import discord
from discord.ext import commands
from discord.ext.commands import bot

class Avatar(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog "Avatar" has been loaded')
    
    @commands.command(aliases=["av"])
    async def avatar(self, ctx, member : commands.MemberConverter):
        embed = discord.Embed(title = f"{member.name}'s profile picture", colour = discord.Colour.blue())
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Avatar(bot))
