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
            "finished": False
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
        
        if server.id not in self.data:
            self.data[server.id] = self.example_server.copy()
            
        if self.data[server.id]["running"]:
            await self.bot.say("Word sprint is already running, cancel it first")
            return
            
        await self.bot.say("Word sprint will begin in **ONE** minute!\nUse `{}sprint join [wc]` to enter!".format(ctx.prefix))

        self.data[server.id]["running"] = True
        
        save_id = self.sprintid
        asyncio.sleep(60)
        
        if save_id != self.sprintid:
            # Can be canceled with another command, so won't start
            return
        
        await self._start_sprint(server, channel, time, ctx.prefix)
        
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
            
        self.data[server.id]["users"][ctx.message.author.id] = [ctx.message.author, wc, wc]

        await self.bot.say("Joined!")
        if self.data[server.id]["started"]:
            await self._time_remaining(server, ctx.message.channel)

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
        
    @sprint.command(name="join", pass_context=True)
    async def sprint_wc(self, ctx, wc: int = 0):
        """
        Post your word count at the end of a sprint
        """
        
        server = ctx.message.server
        if server.id not in self.data:
            self.data[server.id] = self.example_server.copy()

        if self.data[server.id]["running"] or not self.data[server.id]["finished"]:
            await self.bot.say("Not the time to post word counts!")
            return
        
        if ctx.author.id not in self.data[server.id]["users"]:
            await self.bot.say("You are not part of this sprint")
            return
            
        self.data[server.id]["users"][ctx.author.id][2] = wc
        
        await self.bot.say("You wrote {} words during this sprint!".format(wc - self.data[server.id]["users"][ctx.author.id][1]))
        
        await self._wc_ranking(server, channel)

    async def _start_sprint(self, server, channel, time, prefix):
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
            
        # Now do the end sprint stuff
        self.data[server.id]["running"] = False
        
        tag_list = [member[0].mention for member in self.data[server.id]["users"].values()]
        
        await self.bot.send_message(channel, "**Time is UP**\n{}".format(tag_list.join(" ")))
        
        await self.bot.send_message(channel, "You have five minutes to post your final word counts!\nUse `{}sprint wc [word count #]`".format(prefix))
        
        await self._wc_ranking(server, channel)
        
        asyncio.sleep(5*60)
        
        await self.bot.send_message(channel, "Sprint word counts are now final")
        
        await self._wc_ranking(server, channel)
        
        self.sprintid = self.sprintid + 1
        self.data[server.id] = self.example_server.copy()
        
    async def _time_remaining(self, server, channel):
        remaining = datetime.now() - self.data[server.id]["endtime"]
        
        embed=discord.Embed(title="Time Reaming: **{}**".format(remaining))
        
        await self.bot.send_message(channel, embed=embed)
        
    async def _wc_ranking(self, server, channel):
        tot = [[member, start_wc, end_wc, total_wc] 
                for player in self.data[server.id]["users"]
                    for member, start_wc, end_wc, total_wc in player + [player[2]-player[1]]]
        
        tot.sort(key=lambda x : x[3])

        embed=discord.Embed(title="Word Count Totals")
        
        for x in range(len(tot)):
            embed.add_field(name="**#{}**".format(x), value="**{0}** words - {1}\nStarting: {2} - Ending {3}".format(tot[x][3],tot[x][0].mention,tot[x][1],tot[x][2], inline=x>3)
        
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