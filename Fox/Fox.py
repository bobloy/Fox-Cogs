import discord
from discord.ext import commands

class Fox:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
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

def setup(bot):
    bot.add_cog(FoxMain(bot))
