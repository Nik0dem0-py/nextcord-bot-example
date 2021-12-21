from nextcord.ext import commands
from googletrans import Translator
from googletrans.models import Translated, Detected
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class Translate(commands.Cog):
    """
    All Translation commands
    """
    
    
    def __init__(self, bot):
        self.bot = bot


  

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog "Translator" has been loaded.')
    
    @commands.command()
    async def translate(self, ctx, lang, *, thing):
        logger.info("Traslation command used by some dude")
        """Usage: `.translate {destination language} {the sentence you want to translate}`"""
        translator = Translator()
        translation = translator.translate(thing, dest=lang)

        await ctx.reply(f"**`{translation.text}`**")

  


def setup(bot):
    bot.add_cog(Translate(bot))