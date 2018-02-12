import discord
import os
from datetime import datetime,timedelta
from discord.ext import commands

from .utils.dataIO import dataIO
from .utils import checks

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

    @commands.group(aliases=['settimerole'], pass_context=True, no_pm=True)
    @checks.mod_or_permissions(administrator=True)
    async def timeroleset(self, ctx):
        """Adjust timerole settings"""

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @timeroleset.command(pass_context=True, no_pm=True)
    async def addrole(self, ctx, role: discord.Role, days: int, *requiredroles: discord.Role):
        server = ctx.message.server
        if server.id not in self.the_data:
            self.the_data[server.id] = {}
            self.save_data()
        
        
        self.the_data[server.id]['ROLES'] = {role.id: {'DAYS': days}}

        if requiredroles:
            self.the_data[server.id]['ROLES'][role.id]['REQUIRED'] = [r.id for r in requiredroles]

        self.save_data()
        await self.bot.say("Time Role for {0} set to {1} days".format(role.name, days))
    

    async def check_day(self):
        tomorrow = datetime.now()+timedelta(day=1)
        midnight = datetime(year=tomorrow.year, month=tomorrow.month, 
                        day=tomorrow.day, hour=0, minute=0, second=0)
        asyncio.sleep((midnight - datetime.now()).seconds)
        while self is self.bot.get_cog("timerole"):
            for server in self.bot.servers:
                addlist = []
                if server.id not in self.the_data: # Hasn't been configured
                    continue
                
                if not self.the_data[server.id]: # No roles
                    continue
                
                for member in server.members:
                    has_roles = [r.id for r in member.roles]
                    
                    get_roles = [rID for rID in self.the_data[server.id]]
                    
                    check_roles = get_roles - has_roles
                    
                    for role_id in check_roles:
                        # Check for required role
                        if 'REQUIRED' in self.the_data[server.id]['ROLES'][role_id]:  
                            if self.the_data[server.id]['ROLES'][role_id]['REQUIRED'] not in has_roles: 
                                continue
                        
                        
                        if member.joined_at + timedelta(days=self.the_data[server.id]['ROLES'][role_id]['DAYS']) > datetime.today():
                            addlist.append( (member, role_id) )
                
                channel = None
                if "ANNOUNCE" in self.the_data[server.id]:
                    channel = await server.get_channel(self.the_data[server.id])
                
                results = "**These members have received the following roles**\n"
                for member, role_id in addlist:
                    role = discord.Role(id=role_id)
                    await self.bot.add_roles(member, role)
                    results += "{} : {}\n".format(member.display_name, role.name)
                
                if channel:
                    await self.bot.send_message(channel, results)
                    
            asyncio.sleep(86400) # Wait 24 hours
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
    