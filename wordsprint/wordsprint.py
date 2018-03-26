import discord
import asyncio 

from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks

from datetime import datetime,timedelta

import os

class WordSprint:
    """
    Assign roles based on trust rating
    """

    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/wordsprint/sprint_data.json"
        
        self.data = {}
        
        self.sprintid = 0
        
        self.example_server = {
            "running": False,
            "started": False,
            "endtime": None,
            "channel": None
            }
        
    
    @commands.group(pass_context=True, no_pm=True)
    async def sprint(self, ctx):
        """Word sprint base command"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
    
    @checks.mod()
    @sprint.command(name="new", pass_context=True)
    async def sprint_new(self, ctx, time: int):
        """
        Start a new word sprint with set time in minutes
        """
        server = ctx.message.server
        
        await self.bot.say("Word sprint will begin in **ONE** minute!\nUse `{}sprint join [wc]` to enter!".format(ctx.prefix))
        
        if server.id not in self.data:
            self.data[server.id] = self.example_server.copy()
        
        self.data[server.id]["running"] = True
        
        save_id = self.sprintid
        asyncio.sleep(60)
        
        if save_id != self.sprintid:
            # Can be canceled with another command, so won't start
            return
        
        await self._start_sprint(server, channel, time)
        
    @checks.mod()
    @sprint.command(name="cancel", pass_context=True)
    async def sprint_cancel(self, ctx, time: int):
        """
        Cancel the current sprint
        """
        server = ctx.message.server

        if server.id not in self.data:
            self.data[server.id] = self.example_server.copy()
        
        if not self.data[server.id]["running"]:
            await self.bot.say("Nothing to cancel")
        
        else:
            self.sprintid = self.sprintid + 1
            self.data[server.id] = self.example_server.copy()
            
            await self.bot.say("Running sprint has been canceled")

        
    @sprint.command(name="join", pass_context=True)
    async def sprint_join(self, ctx, wc: int = 0):
        """
        Join a running sprint!
        """
        
        server = ctx.message.server
         if server.id not in self.data:
            self.data[server.id] = self.example_server.copy()

        if not self.data[server.id]["running"]:
            await self.bot.say("No sprint running!")
            return
            
        self.data[server.id][ctx.message.author.id] = wc

        dataIO.save_json(self.file_path, self.data)
        
        await self.bot.say("Joined!")
        if self.data[server.id]["started"]:
            await self._time_remaining(ctx.message.channel)

    @sprint.command(name="time", pass_context=True)
    async def sprint_time(self, ctx, wc: int = 0):
        """
        Post the remaining time in a sprint
        """
        server = ctx.message.server
         if server.id not in self.data:
            self.data[server.id] = self.example_server.copy()

        if not self.data[server.id]["running"]:
            await self.bot.say("No sprint running!")
            return

        if not self.data[server.id]["started"]:
            await self.bot.say("Hasn't started yet!")
            return

        await self._time_remaining(server, ctx.message.channel)

    async def _start_sprint(self, server, channel, time):
        duration = timedelta(minutes=time)

        
        self.data[server.id]["channel"] = channel
        
        starttime = datetime.utcnow()
        self.data[server.id]["endtime"] = starttime + duration
        
        await self.bot.send_message(channel, "**Sprint begins now!**")
        await self._time_remaining(server, channel)
        save_id = self.sprintid
        
        asyncio.sleep(time*60)
        
        if save_id != self.sprintid: #Sprint was canceled
            return
        
    async def _time_remaining(self, server, channel):
        remaining = datetime.now() - self.data[server.id]["endtime"]
        
        embed=discord.Embed(title="Time Reaming: **{}**".format(remaining))
        
        await self.bot.send_message(channel, embed=embed)
        

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