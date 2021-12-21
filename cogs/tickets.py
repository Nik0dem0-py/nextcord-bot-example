import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions
import json
import logging
import asyncio

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class Tickets(commands.Cog):
    """
    If help is needed, create a ticket!
    """
    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog "Tickets" has been loaded.')

    @commands.command()
    async def new(self,ctx, *, args = None):
        """This creates a new ticket. Add any words after the command if you'd like to reply a message when we initially create your ticket."""

        await self.bot.wait_until_ready()

        if args == None:
            message_content = "Please wait, we will be with you shortly!"
        
        else:
            message_content = "".join(args)

        with open("cogs/data/tickets.json") as f:
            data = json.load(f)

        ticket_number = int(data["ticket-counter"])
        ticket_number += 1

        ticket_channel = await ctx.guild.create_text_channel("ticket-{}".format(ticket_number))
        await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), reply_messages=False, read_messages=False)

        for role_id in data["valid-roles"]:
            role = ctx.guild.get_role(role_id)

            await ticket_channel.set_permissions(role, reply_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
        
        await ticket_channel.set_permissions(ctx.author, reply_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

        em = nextcord.Embed(title="New ticket from {}#{}".format(ctx.author.name, ctx.author.discriminator), description= "{}".format(message_content), color=0x00a8ff)

        await ticket_channel.reply(embed=em)

        pinged_msg_content = ""
        non_mentionable_roles = []

        if data["pinged-roles"] != []:

            for role_id in data["pinged-roles"]:
                role = ctx.guild.get_role(role_id)

                pinged_msg_content += role.mention
                pinged_msg_content += " "

                if role.mentionable:
                    pass
                else:
                    await role.edit(mentionable=True)
                    non_mentionable_roles.append(role)
            
            await ticket_channel.reply(pinged_msg_content)

            for role in non_mentionable_roles:
                await role.edit(mentionable=False)
        
        data["ticket-channel-ids"].append(ticket_channel.id)

        data["ticket-counter"] = int(ticket_number)
        with open("cogs/data/tickets.json", 'w') as f:
            json.dump(data, f)
        
        created_em = nextcord.Embed(title=" Tickets", description="Your ticket has been created at {}".format(ticket_channel.mention), color=0x00a8ff)
        
        await ctx.reply(embed=created_em)

    @commands.command()
    @has_permissions(administrator=True)
    async def close(self,ctx):
        """Use this to close a ticket. This command only works in ticket channels."""
        with open('cogs/data/tickets.json') as f:
            data = json.load(f)

        if ctx.channel.id in data["ticket-channel-ids"]:

            channel_id = ctx.channel.id

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

            try:

                em = nextcord.Embed(title=" Tickets", description="Are you sure you want to close this ticket? Reply with `close` if you are sure.", color=0x00a8ff)
            
                await ctx.reply(embed=em)
                await self.bot.wait_for('message', check=check, timeout=60)
                await ctx.channel.delete()

                index = data["ticket-channel-ids"].index(channel_id)
                del data["ticket-channel-ids"][index]

                with open('cogs/data/tickets.json', 'w') as f:
                    json.dump(data, f)
            
            except asyncio.TimeoutError:
                em = nextcord.Embed(title=" Tickets", description="You have run out of time to close this ticket. Please run the command again.", color=0x00a8ff)
                await ctx.reply(embed=em)

            

    @commands.command()
    @has_permissions(administrator=True)
    async def addaccess(self,ctx, role_id=None):
        """This can be used to give a specific role access to all tickets. This command can only be run if you have an admin-level role for this bot."""

        with open('cogs/data/tickets.json') as f:
            data = json.load(f)
        
        valid_user = False

        for role_id in data["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        
        if valid_user or ctx.author.guild_permissions.administrator:
            role_id = int(role_id)

            if role_id not in data["valid-roles"]:

                try:
                    role = ctx.guild.get_role(role_id)

                    with open("cogs/data/tickets.json") as f:
                        data = json.load(f)

                    data["valid-roles"].append(role_id)

                    with open('cogs/data/tickets.json', 'w') as f:
                        json.dump(data, f)
                    
                    em = nextcord.Embed(title=" Tickets", description="You have successfully added `{}` to the list of roles with access to tickets.".format(role.name), color=0x00a8ff)

                    await ctx.reply(embed=em)

                except:
                    em = nextcord.Embed(title=" Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                    await ctx.reply(embed=em)
            
            else:
                em = nextcord.Embed(title=" Tickets", description="That role already has access to tickets!", color=0x00a8ff)
                await ctx.reply(embed=em)
        
        else:
            em = nextcord.Embed(title=" Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
            await ctx.reply(embed=em)

    @commands.command()
    @has_permissions(administrator=True)
    async def delaccess(self,ctx, role_id=None):
        """This can be used to remove a specific role's access to all tickets. This command can only be run if you have an admin-level role for this bot."""
        with open('cogs/data/tickets.json') as f:
            data = json.load(f)
        
        valid_user = False

        for role_id in data["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass

        if valid_user or ctx.author.guild_permissions.administrator:

            try:
                role_id = int(role_id)
                role = ctx.guild.get_role(role_id)

                with open("cogs/data/tickets.json") as f:
                    data = json.load(f)

                valid_roles = data["valid-roles"]

                if role_id in valid_roles:
                    index = valid_roles.index(role_id)

                    del valid_roles[index]

                    data["valid-roles"] = valid_roles

                    with open('cogs/data/tickets.json', 'w') as f:
                        json.dump(data, f)

                    em = nextcord.Embed(title=" Tickets", description="You have successfully removed `{}` from the list of roles with access to tickets.".format(role.name), color=0x00a8ff)

                    await ctx.reply(embed=em)
                
                else:
                    
                    em = nextcord.Embed(title=" Tickets", description="That role already doesn't have access to tickets!", color=0x00a8ff)
                    await ctx.reply(embed=em)

            except:
                em = nextcord.Embed(title=" Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                await ctx.reply(embed=em)
        
        else:
            em = nextcord.Embed(title=" Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
            await ctx.reply(embed=em)

    @commands.command()
    @has_permissions(administrator=True)
    async def addpingedrole(self,ctx, role_id=None):
        """This command adds a role to the list of roles that are pinged when a new ticket is created. This command can only be run if you have an admin-level role for this bot."""

        with open('cogs/data/tickets.json') as f:
            data = json.load(f)
        
        valid_user = False

        for role_id in data["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        
        if valid_user or ctx.author.guild_permissions.administrator:

            role_id = int(role_id)

            if role_id not in data["pinged-roles"]:

                try:
                    role = ctx.guild.get_role(role_id)

                    with open("cogs/data/tickets.json") as f:
                        data = json.load(f)

                    data["pinged-roles"].append(role_id)

                    with open('cogs/data/tickets.json', 'w') as f:
                        json.dump(data, f)

                    em = nextcord.Embed(title=" Tickets", description="You have successfully added `{}` to the list of roles that get pinged when new tickets are created!".format(role.name), color=0x00a8ff)

                    await ctx.reply(embed=em)

                except:
                    em = nextcord.Embed(title=" Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                    await ctx.reply(embed=em)
                
            else:
                em = nextcord.Embed(title=" Tickets", description="That role already receives pings when tickets are created.", color=0x00a8ff)
                await ctx.reply(embed=em)
        
        else:
            em = nextcord.Embed(title=" Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
            await ctx.reply(embed=em)

    @commands.command()
    @has_permissions(administrator=True)
    async def delpingedrole(self,ctx, role_id=None):
        """This command removes a role from the list of roles that are pinged when a new ticket is created. This command can only be run if you have an admin-level role for this bot."""

        with open('cogs/data/tickets.json') as f:
            data = json.load(f)
        
        valid_user = False

        for role_id in data["verified-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        
        if valid_user or ctx.author.guild_permissions.administrator:

            try:
                role_id = int(role_id)
                role = ctx.guild.get_role(role_id)

                with open("cogs/data/tickets.json") as f:
                    data = json.load(f)

                pinged_roles = data["pinged-roles"]

                if role_id in pinged_roles:
                    index = pinged_roles.index(role_id)

                    del pinged_roles[index]

                    data["pinged-roles"] = pinged_roles

                    with open('cogs/data/tickets.json', 'w') as f:
                        json.dump(data, f)

                    em = nextcord.Embed(title=" Tickets", description="You have successfully removed `{}` from the list of roles that get pinged when new tickets are created.".format(role.name), color=0x00a8ff)
                    await ctx.reply(embed=em)
                
                else:
                    em = nextcord.Embed(title=" Tickets", description="That role already isn't getting pinged when new tickets are created!", color=0x00a8ff)
                    await ctx.reply(embed=em)

            except:
                em = nextcord.Embed(title=" Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
                await ctx.reply(embed=em)
        
        else:
            em = nextcord.Embed(title=" Tickets", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
            await ctx.reply(embed=em)


    @commands.command()
    @has_permissions(administrator=True)
    async def addadminrole(self,ctx, role_id=None):
        """This command gives all users with a specific role access to the admin-level commands for the bot, such as `.addpingedrole` and `.addaccess`. This command can only be run by users who have administrator permissions for the entire server."""

        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)

            with open("cogs/data/tickets.json") as f:
                data = json.load(f)

            data["verified-roles"].append(role_id)

            with open('cogs/data/tickets.json', 'w') as f:
                json.dump(data, f)
            
            em = nextcord.Embed(title=" Tickets", description="You have successfully added `{}` to the list of roles that can run admin-level commands!".format(role.name), color=0x00a8ff)
            await ctx.reply(embed=em)

        except:
            em = nextcord.Embed(title=" Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
            await ctx.reply(embed=em)

    @commands.command()
    @has_permissions(administrator=True)
    async def deladminrole(self,ctx, role_id=None):
        """This command removes access for all users with the specified role to the admin-level commands for the bot, such as `.addpingedrole` and `.addaccess`. This command can only be run by users who have administrator permissions for the entire server."""
        try:
            role_id = int(role_id)
            role = ctx.guild.get_role(role_id)

            with open("cogs/data/tickets.json") as f:
                data = json.load(f)

            admin_roles = data["verified-roles"]

            if role_id in admin_roles:
                index = admin_roles.index(role_id)

                del admin_roles[index]

                data["verified-roles"] = admin_roles

                with open('cogs/data/tickets.json', 'w') as f:
                    json.dump(data, f)
                
                em = nextcord.Embed(title=" Tickets", description="You have successfully removed `{}` from the list of roles that get pinged when new tickets are created.".format(role.name), color=0x00a8ff)

                await ctx.reply(embed=em)
            
            else:
                em = nextcord.Embed(title=" Tickets", description="That role isn't getting pinged when new tickets are created!", color=0x00a8ff)
                await ctx.reply(embed=em)

        except:
            em = nextcord.Embed(title=" Tickets", description="That isn't a valid role ID. Please try again with a valid role ID.")
            await ctx.reply(embed=em)

def setup(bot):
    bot.add_cog(Tickets(bot))