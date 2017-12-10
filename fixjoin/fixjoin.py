import discord
import os
import math
from discord.ext import commands

from .utils.chat_formatting import pagify
from .utils.chat_formatting import box
from .utils.dataIO import dataIO
from .utils import checks
from random import randint

from datetime import date, datetime, timedelta



class Fixjoin:
    """Cog for organizing flags"""

    def __init__(self, bot):
        self.bot = bot

    @checks.is_owner()
    @commands.command(pass_context=True, no_pm=True)
    async def fixjoin(self, ctx, user: discord.Member, year: int, month: int, day: int):
        """Fix a member's joindate"""
        
        user.joined_at = datetime(year, month, day)
        
        await self.bot.say("Success")

                    
def setup(bot):
    n = Fixjoin(bot)
    bot.add_cog(n)
