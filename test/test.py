import discord
import os
from discord.ext import commands

from .utils.dataIO import dataIO
from .utils import checks

class Test:
    def __init__(self, bot):
        self.bot = bot
        self.path = "data/Fox-Cogs/test"
        self.file_path = "data/Fox-Cogs/test/test.json"
        self.the_data = dataIO.load_json(self.file_path)

    def save_repos(self):
         dataIO.save_json(self.file_path, self.the_data)

    @commands.command()
    async def test(self):
        self.the_data["WOAH"] = True
        save_repos()


def check_folders():
    if not os.path.exists("data/Fox-Cogs"):
        print("Creating data/Fox-Cogs folder...")
        os.makedirs("data/Fox-Cogs")

    if not os.path.exists("data/Fox-Cogs/test"):
        print("Creating data/Fox-Cogs/test folder...")
        os.makedirs("data/Fox-Cogs/test")

        
def check_files():
    if not dataIO.is_valid_json("data/Fox-Cogs/test/test.json"):
        dataIO.save_json("data/Fox-Cogs/test/test.json" ,{})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Fight(bot))
