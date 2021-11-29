import nextcord
from nextcord.ext import commands
import random
import logging

def get_embed(_title, _description, _color):
    return nextcord.Embed(title=_title, description=_description, color=_color)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class Games(commands.Cog):

    """
    Bored? Play one of these games.
    """


    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog "Games" has been loaded.')
    
    @commands.command()
    async def findimposter(self, ctx):
        """
        Impostors can sabotage the reactor, 
        which gives Crewmates 30–45 seconds to resolve the sabotage. 
        If it is not resolved in the allotted time, The Impostor(s) will win.
        """

        embed1 = nextcord.Embed(title = "Who's the imposter?" , description = "Find out who the imposter is, before the reactor breaks down!" , color=0xff0000)
        
        embed1.add_field(name = 'Cream' , value= '<:crewmate_cream:908691460134686741>' , inline=False)
        embed1.add_field(name = 'Purple' , value= '<:crewmate_pastelpurple:908691382682673184>' , inline=False)
        embed1.add_field(name = 'Frosty' , value= '<:FwostyCrewmate:908691296422592573>' , inline=False)
        embed1.add_field(name = 'Orange' , value= '<:Orange_Crewmate:908692685928407060> ' , inline=False)
        
        msg = await ctx.send(embed=embed1)
        
        
        emojis = {
            'Cream': '<:crewmate_cream:908691460134686741>',
            'Purple': '<:crewmate_pastelpurple:908691382682673184>',
            'Frosty': '<:FwostyCrewmate:908691296422592573>',
            'Orange': '<:Orange_Crewmate:908692685928407060>',
        }
        
       
        imposter = random.choice(list(emojis.items()))
        imposter = imposter[0]
        
       
        for emoji in emojis.values():
            await msg.add_reaction(emoji)
        
   
        def check(reaction, user):
            self.reacted = reaction.emoji
            return user == ctx.author and str(reaction.emoji) in emojis.values()

        try: 
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        
        except TimeoutError:
            
            description = "Reactor Meltdown.{0} was the imposter...".format(imposter)
            embed = get_embed("Defeat", description, nextcord.Color.red())
            await ctx.send(embed=embed)
        else:
            
            if str(self.reacted) == emojis[imposter]:
                description = "**{0}** was the imposter...".format(imposter)
                embed = get_embed("Victory", description, nextcord.Color.green())
                await ctx.send(embed=embed)

            
            else:
                for key, value in emojis.items(): 
                    if value == str(self.reacted):
                        description = "**{0}** was not the imposter...".format(key)
                        embed = get_embed("Defeat", description, nextcord.Color.red())
                        await ctx.send(embed=embed)
                        break


def setup(bot):
    bot.add_cog(Games(bot))