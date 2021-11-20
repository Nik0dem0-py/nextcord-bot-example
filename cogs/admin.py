import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from nextcord.errors import Forbidden

class Moderation(commands.Cog):
    """
    Moderation commands for admins/moderators.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog "Moderation" has been loaded.')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, user: nextcord.User, *, message: str):
        """ DM the user of your choice """
        try:
            await user.send(message)
            await ctx.send(f"✉️ Sent a DM to **{user}**")
        except discord.Forbidden:
            await ctx.send("This user might be having DMs blocked or it's a bot account...")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter):
        """Kicks the following member"""
        await ctx.send('What is the reason?')
        msg = await self.bot.wait_for('message')
        reason = msg.content
        description = f'''
        **Member:** = {member}
        **Responsible moderator:** {ctx.author.mention}
        **Reason:** {reason}
        '''

        embed = nextcord.Embed(title='Kick', description=description, colour=nextcord.Colour.green())
        try:
            await member.kick(reason=reason)
            await ctx.send(content=None, embed=embed)
        except Forbidden:
            try:
                await ctx.send("Hey, seems like I can't kick people. Please check my permissions :)")
            except Forbidden:
                await ctx.author.send(
                    f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                    f"May you inform the server team about this issue? :slight_smile: ", embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter):
        """Bans the following member"""
        await ctx.send('What is the reason?')
        msg = await self.bot.wait_for('message')
        reason = msg.content
        description = f'''
        **Member:** = {member}
        **Responsible moderator:** {ctx.author.mention}
        **Reason:** {reason}
        '''

        embed = nextcord.Embed(title='Ban', description=description, colour=nextcord.Colour.green())
        try:
            await member.ban(reason=reason)
            await ctx.send(content=None, embed=embed)
        except Forbidden:
            try:
                await ctx.send("Hey, seems like I can't ban people. Please check my permissions :)")
            except Forbidden:
                await ctx.author.send(
                    f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                    f"May you inform the server team about this issue? :slight_smile: ", embed=embed)









def setup(bot):
    bot.add_cog(Moderation(bot))
