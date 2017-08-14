import discord
import os
from datetime import datetime
from discord.ext import commands

from .utils.dataIO import dataIO
from .utils import checks


class Leaver:
    """Creates a goodbye message when people leave"""

    def __init__(self, bot):
        self.bot = bot
        self.path = "data/Fox-Cogs/leaver"
        self.file_path = "data/Fox-Cogs/leaver/leaver.json"
        self.the_data = dataIO.load_json(self.file_path)


    def save_data(self):
        """Saves the json"""
        dataIO.save_json(self.file_path, self.the_data)

    @commands.group(aliases=['setleaver'], pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def leaverset(self, ctx):
        server = ctx.message.server
        if server.id not in self.the_data:
            self.the_data[server.id] = {}
            self.save_data()

        """Adjust leaver settings"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @leaverset.command(pass_context=True)
    async def channel(self, ctx):
        if 'channel' not in self.the_data[server.id]:
            self.the_data[server.id]['channel'] = ''

        self.the_data[server.id]['channel'] = ctx.message.channel.id
        self.save_data()

    async def on_member_leave(self, member):
        server = member.server
        if server.id not in self.the_data:
            return

        await self.bot.say("YOU LEFT ME "+member.mention)
#        self.the_data[server.id]


def check_folders():
    if not os.path.exists("data/Fox-Cogs"):
        print("Creating data/Fox-Cogs folder...")
        os.makedirs("data/Fox-Cogs")

    if not os.path.exists("data/Fox-Cogs/leaver"):
        print("Creating data/Fox-Cogs/leaver folder...")
        os.makedirs("data/Fox-Cogs/leaver")


def check_files():
    if not dataIO.is_valid_json("data/Fox-Cogs/leaver/leaver.json"):
        dataIO.save_json("data/Fox-Cogs/leaver/leaver.json", {})


def setup(bot):
    check_folders()
    check_files()
    q = Leaver(bot)
    bot.add_cog(q)
    bot.add_listener(n.on_member_leave, "on_member_remove")
