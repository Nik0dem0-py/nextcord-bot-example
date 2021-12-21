from nextcord.ext import commands
import nextcord
import requests
import logging 

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Misc(commands.Cog):
    

    def __init__(self, bot):
        self.bot = bot
        

    @commands.command()
    async def wiki(self, ctx, msg):
        """Usage: .wiki {tesla} or .wiki {elon_musk}"""
        url: str = f"https://en.wikipedia.org/wiki/{msg}"
        await ctx.reply(url)

    @commands.command()
    async def emojis(self, ctx):
        ctx.reply(emojis.guild)


    @commands.command()
    async def length(self, ctx, sent):
        """Counts length of the folowing word/sentece."""
        logger.info(ctx.author.name + sent)
        sentence: str = ctx.message.content[7:]
        print(sentence)
        length: int = len(sentence)
        i = 0
        count: int = 0
        while i < length - 1:
            i += 1
            if sentence[i] == " ":
                count += 1
        word = count + 1
        letter = i + 0
        await ctx.reply(f"World count : {word}, letter count : {letter}")




    @commands.command(aliases=['ud'])
    async def urban(self, ctx, *msg):
        """Searches on the Urban Dictionary."""
        word = ' '.join(msg)
        api = "http://api.urbandictionary.com/v0/define"
        logger.info("Making request to " + api)
        # reply request to the Urban Dictionary API and grab info
        response = requests.get(api, params=[("term", word)]).json()
        embed = nextcord.Embed(description="No results found!", colour=nextcord.Colour.blue())
        if len(response["list"]) == 0:
            return await ctx.reply(embed=embed)
        # Add results to the embed
        embed = nextcord.Embed(title="Word", description=word, colour=nextcord.Colour.blue())
        embed.add_field(name="Top definition:", value=response['list'][0]['definition'])
        embed.add_field(name="Examples:", value=response['list'][0]['example'])
        await ctx.reply(embed=embed)




def setup(bot):
    bot.add_cog(Misc(bot))