import discord
import asyncio 

from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks


class TrustRole:
    """
    Assign roles based on trust rating
    """

    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/trustrole/trust_data.json"
        self.data = dataIO.load_json(self.file_path)
    
    @commands.group(pass_context=True, no_pm=True, aliases=['settrust'])
    @checks.mod_or_permissions(administrator=True)
    async def trustset(self, ctx):
        """Trust settings base command"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @trustset.command(name="trust", pass_context=True)
    async def trustset_trust(self, ctx, role: discord.Role = None, threshold: int = None):
        """
        Set the trust role and threshold
        Run with no arguments to disable trust role assignment
        """
        server = ctx.server
        
        if ctx.server.id not in self.data:
            self.data[server.id] = {"members":{}}
        
        if role is None:
            self.data[server.id]["positive"] = {
                "threshold": None,
                "role_id": None
                }
            await self.bot.say("Trusting is now disabled\nRun `{}help trustset trust` for details".format(ctx.prefix))
            dataIO.save_json(self.file_path, self.data)
            return
        
        if threshold is None or threshold <= 0:
            await self.bot.say("Must provide a threshold >= 0, see `{}help trustset trust` for details".format(ctx.prefix))
            return
        
        self.data[server.id]["positive"] = {
                "threshold": threshold,
                "role_id": role.id
                }
        await self.bot.say("Trusting now assigns {} and is triggered at threshold {}".format(role,threshold))

        dataIO.save_json(self.file_path, self.data)
        
    @trustset.command(name="distrust", pass_context=True)
    async def trustset_distrust(self, ctx, role: discord.Role = None, threshold: int = None):
        """
        Set the distrust role and threshold
        Run with no arguments to disable distrust role assignment
        """
        server = ctx.server
        
        if ctx.server.id not in self.data:
            self.data[server.id] = {"members":{}}
        
        if role is None:
            self.data[server.id]["negative"] = {
                "threshold": None,
                "role_id": None
                }
            await self.bot.say("Distrusting is now disabled\nRun `{}help trustset distrust` for details".format(ctx.prefix))
            dataIO.save_json(self.file_path, self.data)
            return
        
        if threshold is None or threshold <= 0:
            await self.bot.say("Must provide a threshold >= 0, see `{}help trustset distrust` for details".format(ctx.prefix))
            return
        
        self.data[server.id]["negative"] = {
                "threshold": threshold,
                "role_id": role.id
                }
        await self.bot.say("Distrusting now assigns {} and is triggered at threshold {}".format(role,threshold))

        dataIO.save_json(self.file_path, self.data)

    @commands.command(pass_context=True)
    async def trust(self, ctx, member : discord.Member):
        """Vote to trust a user"""
        server = ctx.message.server
        if server.id not in self.data:
            await self.bot.say("This hasn't been setup on this server yet")
            return
            
        if member is ctx.author:
            await self.bot.say("Can't vote for yourself")
            return

        if member.id not in self.data[server.id]["members"]:
            self.data[server.id]["members"][member.id] = {ctx.author.id: 1}
        else:
            self.data[server.id]["members"][member.id][ctx.author.id] = 1
        
        dataIO.save_json(self.file_path, self.data)
        
        await self.bot.say("Voted to trust this user!")
        
        await self.check_trust(member)
        
    @commands.command(pass_context=True)
    async def distrust(self, ctx, member : discord.Member):
        """Vote to distrust a user"""
        server = ctx.message.server
        if server.id not in self.data:
            await self.bot.say("This hasn't been setup on this server yet")
            return
            
        if member is ctx.author:
            await self.bot.say("Can't vote for yourself")
            return

        if member.id not in self.data[server.id]["members"]:
            self.data[server.id]["members"][member.id] = {ctx.author.id: -1}
        else:
            self.data[server.id]["members"][member.id][ctx.author.id] = -1
        
        dataIO.save_json(self.file_path, self.data)
        
        await self.bot.say("Voted to distrust this user!")
        
        await self.check_trust(member)

    async def check_trust(self, member: discord.Member):
        if member.server.id not in self.data:
            return 
            
        server = member.server
        
        if "members" not in self.data[server.id]:
            return
            
        if member.id not in self.data[server.id]["members"]:
            return
        
        trust_level = sum(self.data[server.id]["members"][member.id].values())
        
        for ori in ["positive", "negative"]:
            if ori in self.data[server.id]:
                threshold = self.data[server.id][ori]["threshold"]
                role = None
                if ori == "negative":
                    trust_level = trust_level * -1
                if threshold is not None and trust_level >= threshold:
                    role = discord.utils.get(server.roles, id=self.data[server.id][ori]["role_id"])
                
                if role is not None:
                    await self.bot.add_roles(member, [role])
                
        

def check_folders():
    if not os.path.exists("data/trustrole"):
        print("Creating data/trustrole folder...")
        os.makedirs("data/trustrole")


def check_files():
    f = "data/trustrole/trust_data.json"
    if not dataIO.is_valid_json(f):
        print("Creating empty trust_data.json...")
        dataIO.save_json(f, {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(TrustRole(bot))