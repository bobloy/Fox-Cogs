import discord
import os
from discord.ext import commands

from .utils.dataIO import dataIO
from .utils import checks

class Fight:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.path = "data/Fox-Cogs/fight/"
        self.file_path = "data/Fox-Cogs/fight/fight.json"
        self.the_data = dataIO.load__json(self.file_path)
        self.fights = 
    @commands.group(pass_context=True)
    async def fight(self, ctx):
        """This does stuff!"""

        #Your code will go here
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
        #await self.bot.say("I can do stuff!")


    @fight.command()
    async def join(self, ctx):
        """Join the active brawl"""
        #Your code will go here
        if not user:
            user = ctx.message.author
        await self.bot.say("ONE PUNCH! And " + user.mention + " is out! ლ(ಠ益ಠლ)")

    @fight.command()
    async def score(self):
        """Enters score for current game"""
        await self.bot.say("Todo")

    @fight.command()
    async def leave(self):
        """Forfeit your match and all future matches"""
        await self.bot.say("Todo")

    @fight.command()
    async def leaderboard(self, ctag, ckind = "Unranked", irank = 0):
        """Adds clan to grab-list"""
        await self.bot.say("Todo")

    @fight.group(pass_context=True)
    async def bracket(self, ctag):
        """Removes clan from future data grabs"""
        await self.bot.say("Todo")

        #Your code will go here
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
        #await self.bot.say("I can do stuff!")

    @bracket.command()
    async def full(self, ctag):
         """Adds clan to grab-list"""
        await self.bot.say("Todo")


     @commands.group(pass_context=True)
     async def setfight(self, ctx):
        """This does stuff!"""

        #Your code will go here
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
        #await self.bot.say("I can do stuff!")


     @setfight.command()
     async def score(self):
        """Prints low trophy users for all registered clans"""
        await self.bot.say("Todo")

    async def _getclanstats(self):
        await self.bot.say("Getclanstats Todo")

    async def _gettrophy(self):
        await self.bot.say("Gettrophy Todo")

    async def _parseclanstats(self):
        await self.bot.say("Parseclanstats Todo")

    async def _parsedate(self):
        await self.bot.say("Parsedate Todo")

    async def _parsemember(self):
        await self.bot.say("Parsemember Todo")
    
def check_folders():
    if not os.path.exists("data/Fox-Cogs"):
        print("Creating data/Fox-Cogs folder...")
        os.makedirs("data/Fox-Cogs")

    if not os.path.exists("data/Fox-Cogs/fight"):
        print("Creating data/Fox-Cogs/fight folder...")
        os.makedirs("data/Fox-Cogs/fight")


def check_files():
    if not dataIO.is_valid_json("data/Fox-Cogs/fight/fight.json"):
        dataIO.save_json("data/Fox-Cogs/fight/fight.json" ,{})
    

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Fight(bot))
