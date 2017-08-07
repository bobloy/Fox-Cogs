import discord
import os
from discord.ext import commands

from .utils.dataIO import dataIO
from .utils import checks


class Fight:
    """Cog for organizing tournaments"""

    def __init__(self, bot):
        self.bot = bot
        self.path = "data/Fox-Cogs/fight/"
        self.file_path = "data/Fox-Cogs/fight/fight.json"
        self.the_data = dataIO.load__json(self.file_path)


#**********************Fight command group start*********************
    @commands.group(pass_context=True, no_pm=True)
    async def fight(self, ctx):
        """Participate in active tournaments!"""

        #Your code will go here
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
            #await self.bot.say("I can do stuff!")

    @fight.command(name="join")
    async def fight_join(self, ctx, user: discord.Member):
        """Join the active brawl"""
        #Your code will go here
        if not user:
            user = ctx.message.author
        await self.bot.say("ONE PUNCH! And " + user.mention + " is out! ლ(ಠ益ಠლ)")

    @fight.command()
    async def score(self, ctx):
        """Enters score for current match, or for passed game ID"""
        await self.bot.say("Todo Score")

    @fight.command()
    async def leave(self):
        """Forfeit your match and all future matches"""
        await self.bot.say("Todo Leave")

    @fight.command()
    async def leaderboard(self, ctag, ckind="Unranked", irank=0):
        """Adds clan to grab-list"""
        await self.bot.say("Todo Leaderboard")

    @fight.group(pass_context=True)
    async def bracket(self, ctx, ctag):
        """Shows your current match your next opponent, run bracket full to see all matches"""
        await self.bot.say("Todo Bracket")

        #Your code will go here
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
        #await self.bot.say("I can do stuff!")

    @bracket.command()
    async def full(self, ctag):
        """Shows the full bracket"""
        await self.bot.say("Todo Bracket Full")
#**********************Fight command group end**************************

#**********************Fightset command group start*********************
    @commands.group(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(administrator=True)
    async def fightset(self, ctx):
        """Admin command for starting or managing tournaments"""

        #Your code will go here
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
        #await self.bot.say("I can do stuff!")

    @fightset.command()
    async def score(self):
        """Prints low trophy users for all registered clans"""
        await self.bot.say("Todo Fightset Score")
#**********************Fightset command group end*********************

    async def _activefight(self):
        """Checks if there is an active tournament already"""
        await self.bot.say("_activefight Todo")

    async def _infight(self, user: discord.Member):
        """Checks if passed member is already in the tournament"""
        await self.bot.say("_infight Todo")

    async def _openregistration(self):
        """Checks if tournament is accepting joins"""
        await self.bot.say("_openregistration Todo")

    async def _comparescores(self):
        """Checks user submitted scores for inconsistancies"""
        await self.bot.say("_comparescores Todo")

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
        dataIO.save_json("data/Fox-Cogs/fight/fight.json", {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Fight(bot))
