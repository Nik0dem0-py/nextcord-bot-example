import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from nextcord.errors import Forbidden
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

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
    async def dm(self, ctx, user: commands.MemberConverter, *, message: str):
        """ DM the user of your choice """
        try:
            await user.send(message)
            await ctx.reply(f"✉️ Sent a DM to **{user}**")
        except nextcord.Forbidden:
            await ctx.reply("This user might be having DMs blocked or it's a bot account...")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter):
        """Kicks the following member"""
        await ctx.reply('What is the reason?')
        msg = await self.bot.wait_for('message')
        reason = msg.content
        description = f'''
        **Member:**  {member}
        **Responsible moderator:** {ctx.author.mention}
        **Reason:** {reason}
        '''
        logger.info(description)

        embed = nextcord.Embed(title='Kick', description=description, colour=nextcord.Colour.green())
        try:
            await member.kick(reason=reason)
            await ctx.reply(content=None, embed=embed)
        except Forbidden:
            try:
                await ctx.reply("Hey, seems like I can't kick people. Please check my permissions :)")
            except Forbidden:
                await ctx.author.send(
                    f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                    f"May you inform the server team about this issue? :slight_smile: ", embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter):
        """Bans the following member"""
        await ctx.reply('What is the reason?')
        msg = await self.bot.wait_for('message')
        reason = msg.content
        description = f'''
        **Member:**  {member}
        **Responsible moderator:** {ctx.author.mention}
        **Reason:** {reason}
        '''
        logger.info(description)

        embed = nextcord.Embed(title='Ban', description=description, colour=nextcord.Colour.green())
        embed.set_image(url="https://tenor.com/view/bongocat-banhammer-ban-hammer-bongo-gif-18219363")
        try:
            await member.ban(reason=reason)
            await ctx.reply(content=None, embed=embed)
        except Forbidden:
            try:
                await ctx.reply("Hey, seems like I can't ban people. Please check my permissions :)")
            except Forbidden:
                await ctx.author.send(
                    f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                    f"May you inform the server team about this issue? :slight_smile: ", embed=embed)



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.reply(f'User {user.mention} has been unbanned')
                logger.info(f"User {user} has been unbanned")
                return

    @commands.command()
    @has_permissions(administrator=True)
    async def lockdown(self, ctx, role : commands.RoleConverter):
        role = ctx.guild.roles[1] 
        perms = nextcord.Permissions(view_channel= False)
        await role.edit(permissions=perms)   
        await ctx.reply("**Full server lockdown iniciated.**")
        logger.info(f"{guild.name} on lockdown")



    @commands.command()
    @has_permissions(administrator=True)
    async def unlock(self, ctx, role : commands.RoleConverter):
        role = ctx.guild.roles[1] 
        perms = nextcord.Permissions(view_channel= True)
        await role.edit(permissions=perms)
        await ctx.reply("**Server has been unlocked.**")       



def setup(bot):
    bot.add_cog(Moderation(bot))
