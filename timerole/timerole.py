import discord
import os
from datetime import datetime,timedelta
from discord.ext import commands

from .utils.dataIO import dataIO
from .utils import checks
from .utils.chat_formatting import box
from .utils.chat_formatting import pagify

import asyncio

class Timerole:
    """Creates a goodbye message when people leave"""

    def __init__(self, bot):
        self.bot = bot
        self.path = "data/Fox-Cogs/timerole"
        self.file_path = "data/Fox-Cogs/timerole/timerole.json"
        self.the_data = dataIO.load_json(self.file_path)

    def save_data(self):
        """Saves the json"""
        dataIO.save_json(self.file_path, self.the_data)
    
    @commands.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def runtimerole(self, ctx):
        """Trigger the daily timerole"""
        
        await self.timerole_update()
        await self.bot.say("Success")
    @commands.group(aliases=['settimerole'], pass_context=True, no_pm=True)
    @checks.mod_or_permissions(administrator=True)
    async def timeroleset(self, ctx):
        """Adjust timerole settings"""

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @timeroleset.command(pass_context=True, no_pm=True)
    async def addrole(self, ctx, role: discord.Role, days: int, *requiredroles: discord.Role):
        """Add a role to be added after specified time on server"""
        server = ctx.message.server
        if server.id not in self.the_data:
            self.the_data[server.id] = {}
            self.save_data()
        
        
        self.the_data[server.id]['ROLES'] = {role.id: {'DAYS': days}}

        if requiredroles:
            self.the_data[server.id]['ROLES'][role.id]['REQUIRED'] = [r.id for r in requiredroles]

        self.save_data()
        await self.bot.say("Time Role for {0} set to {1} days".format(role.name, days))
        
    @timeroleset.command(pass_context=True, no_pm=True)
    async def channel(self, ctx, channel: discord.Channel):
        """Sets the announce channel for role adds"""
        server = ctx.message.server
        if server.id not in self.the_data:
            self.the_data[server.id] = {}
            self.save_data()
        
        
        self.the_data[server.id]['ANNOUNCE'] = channel.id

        self.save_data()
        await self.bot.say("Announce channel set to {0}".format(channel.mention))
    
    
    async def timerole_update(self):
        for server in self.bot.servers:
            print("In server {}".format(server.name))
            addlist = []
            if server.id not in self.the_data: # Hasn't been configured
                print("Not configured")
                continue
            
            if 'ROLES' not in self.the_data[server.id]: # No roles
                print("No roles")
                continue
            
            for member in server.members:
                has_roles = [r.id for r in member.roles]
                
                get_roles = [rID for rID in self.the_data[server.id]['ROLES']]
                
                check_roles = set(get_roles) - set(has_roles)
                
                print("{} is being checked for {}".format(member.display_name, check_roles))
                
                for role_id in check_roles:
                    # Check for required role
                    if 'REQUIRED' in self.the_data[server.id]['ROLES'][role_id]:
                        if not set(self.the_data[server.id]['ROLES'][role_id]['REQUIRED']) & set(has_roles): 
                            print("Doesn't have required role")
                            continue
                    
                    
                    if member.joined_at + timedelta(days=self.the_data[server.id]['ROLES'][role_id]['DAYS']) > datetime.today():
                        print("Qualifies")
                        addlist.append( (member, role_id) )
                    print("Out")
            channel = None
            if "ANNOUNCE" in self.the_data[server.id]:
                channel = server.get_channel(self.the_data[server.id]["ANNOUNCE"])
            
            results = "**These members have received the following roles**\n"
            for member, role_id in addlist:
                role = discord.utils.get(server.roles, id=role_id)
                await self.bot.add_roles(member, role)
                results += "{} : {}\n".format(member.display_name, role.name)
            
            if channel:
                for page in pagify(
                        results, shorten_by=50):
                    await self.bot.send_message(channel, page)
                
            print(results)
            
    async def check_day(self):
        tomorrow = datetime.now()+timedelta(days=1)
        midnight = datetime(year=tomorrow.year, month=tomorrow.month, 
                        day=tomorrow.day, hour=0, minute=0, second=0)

        await asyncio.sleep((midnight - datetime.now()).seconds)
        print("About to start")
        while self is self.bot.get_cog("Timerole"):
        
            await self.timerole_update()
            
            await asyncio.sleep(86400) # Wait 24 hours


def check_folders():
    if not os.path.exists("data/Fox-Cogs"):
        print("Creating data/Fox-Cogs folder...")
        os.makedirs("data/Fox-Cogs")

    if not os.path.exists("data/Fox-Cogs/timerole"):
        print("Creating data/Fox-Cogs/timerole folder...")
        os.makedirs("data/Fox-Cogs/timerole")


def check_files():
    if not dataIO.is_valid_json("data/Fox-Cogs/timerole/timerole.json"):
        dataIO.save_json("data/Fox-Cogs/timerole/timerole.json", {})


def setup(bot):
    check_folders()
    check_files()
    q = Timerole(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(q.check_day())
    bot.add_cog(q)
    