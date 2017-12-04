import discord
import os
import math
from discord.ext import commands

from .utils.chat_formatting import pagify
from .utils.chat_formatting import box
from .utils.dataIO import dataIO
from .utils import checks
from random import randint

from datetime import date, timedelta



class Flag:
    """Cog for organizing flags"""

    def __init__(self, bot):
        self.bot = bot
        self.path = "data/Fox-Cogs/flag/"
        self.file_path = "data/Fox-Cogs/flag/flag.json"
        self.the_data = dataIO.load_json(self.file_path)
        # self.tags = dataIO.load_json("cogs/tags.json")
        # self.clans = dataIO.load_json("cogs/clans.json")


    def save_data(self):
        """Saves the json"""
        dataIO.save_json(self.file_path, self.the_data)

    def _flag_template(self):
        return {
            'reason': None,
            'expireyear': None,
            'expiremonth': None,
            'expireday': None
            }
# ************************Flag command group start************************
    @commands.command(pass_context=True, no_pm=True)
    async def flag(self, ctx, user: discord.Member, *reason):
        """Flag a user"""
        server = ctx.message.server
        self._check_flags(server)
        # clashroyale = self.bot.get_cog('clashroyale')
        # if clashroyale is None:
            # await self.bot.say("Requires clashroyale cog installed")
            # return
            
        if user.id not in self.the_data[server.id]['flags']:
            self.the_data[server.id]['flags'][user.id] = []
        
        flag = self._flag_template()
        expiredate = date.today() 
        expiredate += timedelta(days=self.the_data[server.id]['days'])
        
        flag['reason'] = " ".join(reason)
        flag['expireyear'] = expiredate.year
        flag['expiremonth'] = expiredate.month
        flag['expireday'] = expiredate.day
        
        self.the_data[server.id]['flags'][user.id].append(flag)
        self.save_data()
        await self._list_flags(ctx, server, user)
    
@commands.command(pass_context=True, no_pm=True, aliases['flagclear'])
    async def clearflag(self, ctx, user: discord.Member):
        """Clears flags for a user"""
        server = ctx.message.server
        self._check_flags(server)

        self.the_data[server.id]['flags'][user.id] = []
        
        self.save_data()
        await self.bot.say("Success!") 
    
    @checks.mod_or_permissions(administrator=True)
    @commands.group(pass_context=True, no_pm=True, aliases=['setflag'])
    async def flagset(self, ctx):
        """Manage settings for flagging"""
        server = ctx.message.server
        self._check_flags(server)
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
            
        # clashroyale = self.bot.get_cog('clashroyale')
        # if clashroyale is None:
            # await self.bot.say("Requires clashroyale cog installed")
            # return
            
        
            
    @flagset.command(pass_context=True, no_pm=True, name="expire")
    async def flagset_expire(self, ctx, days: int):
        """Set the number of days for flags to expire after for server"""
        server = ctx.message.server
        self.the_data[server.id]['days'] = days
        self.save_data()
        await self.bot.say("Success")
        
    async def _list_flags(self, ctx, server, user):
        """Sends a pretty embed of flags on a user to context"""
        if user.id not in self.the_data[server.id]['flags']:
            await self.bot.send_message(ctx.message.channel, "This user has no flags!")
            return

        embed=discord.Embed(title="Flags for "+user.mention, description="User has "+str(len(self.the_data[server.id]['flags'][user.id]))+" active flags", color=0x804040)
        for flag in self.the_data[server.id]['flags'][user.id]:
            embed.add_field(name="Reason: "+flag['reason'], value="Expires on "+str(date(flag['expireyear'], flag['expiremonth'], flag['expireday'])), inline=True)
        
        await self.bot.send_message(ctx.message.channel, embed=embed)


    def _check_flags(self, server):
        """Updates and removes expired flags"""
        if server.id not in self.the_data:
            self.the_data[server.id] = {
                'flags': {},
                'days': 31
                }

        for userid in self.the_data[server.id]['flags']:
            x = 0
            while x < len(self.the_data[server.id]['flags'][userid]):
                flag = self.the_data[server.id]['flags'][userid][x]
                if date.today() >= date(flag['expireyear'], flag['expiremonth'], flag['expireday']):
                    self.the_data[server.id]['flags'][userid].pop(x)
                else:
                    x += 1
                    
        self.save_data()
                    
def check_folders():
    if not os.path.exists("data/Fox-Cogs"):
        print("Creating data/Fox-Cogs folder...")
        os.makedirs("data/Fox-Cogs")

    if not os.path.exists("data/Fox-Cogs/flag"):
        print("Creating data/Fox-Cogs/flag folder...")
        os.makedirs("data/Fox-Cogs/flag")


def check_files():
    flagjson = {
        'flags': {},
        'settings': {}
        }
    if not dataIO.is_valid_json("data/Fox-Cogs/flag/flag.json"):
        dataIO.save_json("data/Fox-Cogs/flag/flag.json", {})


def setup(bot):
    check_folders()
    check_files()
    n = Flag(bot)
    bot.add_cog(n)
