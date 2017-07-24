import discord
import os
from discord.ext import commands

from .utils.dataIO import dataIO
from .utils import checks

class Fox:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def fox(self, ctx):
        """This does stuff!"""

        #Your code will go here
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
        #await self.bot.say("I can do stuff!")


    @fox.command()
    async def punch(self, user : discord.Member):
        """I will puch anyone! >.<"""
        #Your code will go here
        await self.bot.say("ONE PUNCH! And " + user.mention + " is out! ლ(ಠ益ಠლ)")

    @fox.command()
    async def lowtrophy(self):
        """Prints low trophy users for all registered clans"""
        await self.bot.say("Todo")

    @fox.command()
    async def gettrophy(self):
        """Gets fresh data from Clashstat"""
        await self.bot.say("Todo")

    @fox.command()
    async def addclan(self, ctag, ckind = "Unranked", irank = 0):
        """Adds clan to grab-list"""
        await self.bot.say("Todo")

    @fox.command()
    async def removeclan(self, ctag):
        """Removes clan from future data grabs"""
        await self.bot.say("Todo")

    async def getclanstats(self):
        await self.bot.say("Getclanstats Todo")

    async def gettrophy(self):
        await self.bot.say("Gettrophy Todo")

    async def parseclanstats(self):
        await self.bot.say("Parseclanstats Todo")

    async def parsedate(self):
        await self.bot.say("Parsedate Todo")

    async def parsemember(self):
        await self.bot.say("Parsemember Todo")
    
def check_folders():
    if not os.path.exists("data/Fox-Cogs"):
        print("Creating data/Fox-Cogs folder...")
        os.makedirs("data/Fox-Cogs")

    if not os.path.exists("data/Fox-Cogs/fox"):
        print("Creating data/Fox-Cogs/fox folder...")
        os.makedirs("data/Fox-Cogs/fox")


def check_files():
    if not dataIO.is_valid_json("data/Fox-Cogs/fox/fox.json"):
        dataIO.save_json("data/Fox-Cogs/fox/fox.json" ,{})
    

def setup(bot):
    bot.add_cog(Fox(bot))
