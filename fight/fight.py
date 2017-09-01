import discord
import os
from discord.ext import commands

from .utils.dataIO import dataIO
from .utils import checks
from random import randint


# 0 - Robin, 1 - Single, 2 - Double, 3 - Triple, 4 - Guarentee, 5 - Compass
T_TYPES = ["Round Robin", "Single Elimination", "Double Elimination", "Triple Elimination", "3 Game Guarentee", "Compass Draw"]


class Fight:
    """Cog for organizing tournaments"""

    def __init__(self, bot):
        self.bot = bot
        self.path = "data/Fox-Cogs/fight/"
        self.file_path = "data/Fox-Cogs/fight/fight.json"
        self.the_data = dataIO.load_json(self.file_path)
    
    def save_data(self):
        """Saves the json"""
        dataIO.save_json(self.file_path, self.the_data)


# ************************Fight command group start************************
    @commands.group(pass_context=True, no_pm=True)
    async def fight(self, ctx):
        """Participate in active tournaments!"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
            # await self.bot.say("I can do stuff!")
        
        server = ctx.message.server
        
        if self._currTourny(server):
            await self.bot.say("No tournament currently running!")
        else:
            currTourny = self.the_data[server.id]["TOURNEYS"][self.the_data[server.id]["CURRENT"]]

    @fight.command(name="join")
    async def fight_join(self, ctx, user: discord.Member):
        """Join the active brawl"""
        # Your code will go here
        if not user:
            user = ctx.message.author
        await self.bot.say("ONE PUNCH! And " + user.mention + " is out! ლ(ಠ益ಠლ)")

    @fight.command()
    async def score(self, ctx, gameID):
        if gameID is None:
            if ctx.message.author not in currTourny["PLAYERS"]:
                await self.bot.say("You are not in a current tournament")
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
        """Shows your current match your next opponent,
            run [p]fight bracket full to see all matches"""
        await self.bot.say("Todo Bracket")

        # Your code will go here
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
        # await self.bot.say("I can do stuff!")

    @bracket.command()
    async def full(self, ctag):
        """Shows the full bracket"""
        await self.bot.say("Todo Bracket Full")

# **********************Fightset command group start*********************
    @commands.group(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(administrator=True)
    async def fightset(self, ctx):
        """Admin command for starting or managing tournaments"""
        server = ctx.message.server

        if server.id not in self.the_data:
            self.the_data[server.id] = {
                "CURRENT": None,
                "TOURNEYS": []
            }
            self.save_data()

        currServ = self.the_data[server.id]

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
        # await self.bot.say("I can do stuff!")
    
    @fightset.command()
    async def bestof(self, incount):
        """Adjust # of games played per match. Must be an odd number"""
        await self.bot.say("Todo Fightset Bestof")
        
    @fightset.command()
    async def bestoffinal(self):
        """Adjust # of games played in finals. Must be an odd number
        (Does not apply to tournament types without finals, such as Round Robin)"""
        await self.bot.say("Todo Fightset Score")
        
    @fightset.command()
    async def setup(self):
        """Setup a new tournament!
        Default settings are as follows
        Name: Tourny # (counts from 0)
        Best of: 1
        Best of (final): 1
        Self Report: True
        Type: 0 (Round Robin)"""
        
        tourID = len(currServ["TOURNEYS"])  # Can just be len without +1, tourny 0 makes len 1, tourny 1 makes len 2, etc
        currServ["CURRENT"] = tourID
        currServ["TOURNEYS"][tourID] = ["PLAYERS": [], "NAME": "Tourney "+str(tourID), "RULES": ["BESTOF": 1, "BESTOFFINAL": 1, "SELFREPORT": True, "TYPE": 0], "TYPEDATA": []]
        
        self.save_data()
        
        self._rr_setup(tourID)
        
    @fightset.command()
    async def stop(self):
        """Stops current tournament"""
        currServ["CURRENT"] = None
        await self.bot.say("Todo Fightset Stop")

# **********************Private command group start*********************
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
        
    def _get_server_from_id(self, serverid):
        return discord.utils.get(self.bot.servers, id=serverid)
        
    def _currTourny(self, server):
        return self.the_data[server.id]["CURRENT"] is None

# **********************Single Elimination***************************
    async def _elim_setup(self, tID):
        await self.bot.say("Elim setup todo")
    
    async def _elim_start(self, tID):
        await self.bot.say("Elim start todo")

    async def _elim_update(self, matchID, ):
        await self.bot.say("Elim update todo")
        
        
# **********************Round-Robin**********************************
    async def _rr_setup(self, tID):
    
        theT = self.the_data["TOURNEYS"][tID]
        
        theD = theT["TYPEDATA"]
        
        theD = []
        
        await self.bot.say("RR setup todo")
    
    async def _rr_start(self, tID):
        theT = self.the_data["TOURNEYS"]
        await self.bot.say("RR start todo")
    
    async def _rr_update(self, matchID, ):
        await self.bot.say("rr update todo")
        
    def _rr_schedule(inlist):
        """ Create a schedule for the teams in the list and return it"""
        s = []
        
        if len(inlist) % 2 == 1: 
            inlist = inlist + ["BYE"]

        for i in range(len(inlist)-1):

            mid = int(len(inlist) / 2)
            l1 = inlist[:mid]
            l2 = inlist[mid:]
            l2.reverse()
            
            matchLetter=""
            firstID = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

            j = i
            
            while j+1 > 26:
            
                matchLetter += firstID[int(j + 1) % 26 - 1]
                
                j = (j + 1) / 26 - 1
                
            matchLetter += firstID[int(j+1) % 26-1]
            
            matchLetter = matchLetter[::-1]
                
            matchID = []    
                
            for ix in range(len(l1)-1):

                matchID += [matchLetter+str(ix)]

            s = s + [list(zip(l1, l2, matchID))]

            inlist.insert(1, inlist.pop())

        return s


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
