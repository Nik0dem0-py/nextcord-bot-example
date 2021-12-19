import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import bot
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class User(commands.Cog):
    """
    User information
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog "User" has been loaded')
    
    @commands.command(name="avatar", descritpion="Shows following member's profile picture", aliases=["av"])
    async def _avatar(self, ctx, member : commands.MemberConverter):
        logger.info("Avatar command used to show " + member)
        """Shows following member's profile picture"""
        embed = nextcord.Embed(title = f"{member.name}'s profile picture", colour = nextcord.Colour.blue())
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="userinfo", descritpion="Shows information about the following member", aliases=['user'])
    async def info(self, ctx, member : commands.MemberConverter):
        logger.info("Info command used to show info of " + member)
        """Shows information about the following member"""
       
        embed = nextcord.Embed(
            title=f"About {member.name}", 
            description = f"ID: `{member.id}`\n Name: `{member.name}#{member.discriminator}` \n Avatar URL: [click!]({member.avatar_url})", 
            colour = nextcord.Colour.blue())
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(User(bot))
