import discord

from discord.ext import commands

from .utils.chat_formatting import pagify
from .utils.chat_formatting import box

from howdoi import howdoi


class Howdoi:
    """Cog for answering coding questions"""

    def __init__(self, bot):
        self.bot = bot
        self.query = ""
        self.args = {
            "query": self.query,
            "pos": 1,
            "all": False,
            "link": False,
            "color": False,
            "num_answers": 1,
            "clear_cache": False,
            "version": False
            }

    @commands.command(pass_context=True)
    async def howdoi(self, ctx, *question):
        """Ask a coding question"""
        self.query = " ".join(question)
        
        self.args["query"] = self.query
        
        out = howdoi.howdoi(self.args).encode('utf-8', 'ignore')
        
        for page in pagify(out, shorten_by=24):
            await self.bot.say(box(page))
        
def setup(bot):
    n = Howdoi(bot)
    bot.add_cog(n)
