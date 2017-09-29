import discord
import os
import math
from discord.ext import commands

from .utils.dataIO import dataIO
from .utils import checks
from random import randint


# 0 - Robin, 1 - Single, 2 - Double, 3 - Triple, 4 - Guarentee, 5 - Compass
T_TYPES = ["Round Robin", "Single Elimination",
           "Double Elimination", "Triple Elimination",
           "3 Game Guarentee", "Compass Draw"]


class Fight:
    """Cog for organizing fights"""

    def __init__(self, bot):
        self.bot = bot
        self.path = "data/Fox-Cogs/fight/"
        self.file_path = "data/Fox-Cogs/fight/fight.json"
        self.the_data = dataIO.load_json(self.file_path)
        self.server = None
        
    def save_data(self):
        """Saves the json"""
        dataIO.save_json(self.file_path, self.the_data)


# ************************Fight command group start************************
    @commands.group(pass_context=True, no_pm=True)
    async def fight(self, ctx):
        """Participate in active fights!"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
            # await self.bot.say("I can do stuff!")

        self.server = ctx.message.server

        if self._isrunningFight(self.server):
            await self.bot.say("No tournament currently running!")
        else:
            await self.bot.say("Current tournament ID: " + self.the_data[self.server.id]["TOURNEYS"][self.the_data[self.server.id]["CURRENT"]])

    @fight.command(name="join", pass_context=True)
    async def fight_join(self, ctx, user: discord.Member):
        """Join the active brawl"""
        # Your code will go here
        if not user:
            user = ctx.message.author

        if self._isrunningFight(self.server):
            await self.bot.say("No tournament currently running!")
        else:
            currFight = self.the_data[self.server.id]["TOURNEYS"][self.the_data[self.server.id]["CURRENT"]]

    @fight.command(name="score", pass_context=True)
    async def fight_score(self, ctx, gameID):
        if gameID is None:
            if ctx.message.author not in currFight["PLAYERS"]:
                await self.bot.say("You are not in a current tournament")
        """Enters score for current match, or for passed game ID"""
        await self.bot.say("Todo Score")

    @fight.command(name="leave", pass_context=True)
    async def fight_leave(self, ctx):
        """Forfeit your match and all future matches"""
        await self.bot.say("Todo Leave")

#    @fight.command(name="leaderboard", pass_context=True)
#    async def fight_leaderboard(self, ctx, ctag, ckind="Unranked", irank=0):
#        """Adds clan to grab-list"""
#        await self.bot.say("Todo Leaderboard")

    @fight.group(name="bracket", pass_context=True)
    async def fight_bracket(self, ctx, ctag):
        """Shows your current match your next opponent,
            run [p]fight bracket full to see all matches"""
        await self.bot.say("Todo Bracket")

        # Your code will go here
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
        # await self.bot.say("I can do stuff!")

    @fight_bracket.command(name="full")
    async def fight_bracket_full(self, ctag):
        """Shows the full bracket"""
        await self.bot.say("Todo Bracket Full")

# **********************Fightset command group start*********************
#    def fightsetdec(func):
#        async def decorated(self, ctx, *args, **kwargs):
#            server = ctx.message.server
#            await func(self, ctx, server, *args, **kwargs)
#        return decorated

    @commands.group(pass_context=True, no_pm=True, aliases=['setfight'])
    @checks.mod_or_permissions(administrator=True)
    async def fightset(self, ctx):
        """Admin command for starting or managing tournaments"""
        self.server = ctx.message.server
        
        if self.server.id not in self.the_data:
            self.the_data[self.server.id] = {
                "CURRENT": None,
                "TOURNEYS": {}
            }
            self.save_data()

        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
        # await self.bot.say("I can do stuff!")

    @fightset.command(name="bestof", pass_context=True)
    async def fightset_bestof(self, ctx, incount):
        """Adjust # of games played per match. Must be an odd number"""
        if not self._activefight():
            await self.bot.say("No active fight to adjust")
            return

        try:
            num = int(incount)
        except:
            await self.bot.say("That is not a number")
            return

        await self.bot.say("Todo Fightset Bestof")

    @fightset.command(name="bestoffinal")
    async def fightset_bestoffinal(self, gamenum):
        """Adjust # of games played in finals. Must be an odd number
        (Does not apply to tournament types without finals, such as Round Robin)"""
        if not self._activefight():
            await self.bot.say("No active fight to adjust")
            return
        
        try:
            gamenum = int(gamenum)
        except:
            await self.bot.say("Must be a number")
            return

        if gamenum % 2 >= 1:
            await self.bot.say("Must be an odd number")
            return
            
        currFight = _getcurrentFight(self.server)
        
        currFight["RULES"]["BESTOF"] = gamenum
        
        self.save_data()
        
        await self.bot.say("Tournament BestOf is now set to:" + str(currFight["RULES"]["BESTOF"]))
    
    @fightset.command(name="current")
    async def fightset_current(self, tID):
        """Sets the current tournament to passed ID"""
        try:
            getFight = self.the_data[self.server.id]["TOURNEYS"][tID]
            
        except:
            await self.bot.say("No tourney found with that ID")
         
        self.the_data[self.server.id]["CURRENT"] = tID
        self.save_data()
        
        await self.bot.say("Current tournament set to "+tID)
        
    @fightset.command(name="list", pass_context = True )
    async def fightset_list(self, ctx):
        """Lists all current and past fights"""
        
        for fight in self.the_data[self.server.id]["TOURNEYS"]:
            await self.bot.say(fight)
        
        await self.bot.say("Done")
        
    @fightset.command(name="toggleopen")
    async def fightset_toggleopen(self):
        """Toggles the open status of current tournament"""
        
        await self.bot.say(self.server.id)
        isActive = self._activefight()
        await self.bot.say(isActive)
        if isActive:
            await self.bot.say("No active fight to adjust")
            return
        
        currFight = _getcurrentFight(self.server)
        
        currFight["OPEN"] = not currFight["OPEN"]
        
        self.save_data()
        
        await self.bot.say("Tournament Open status is now set to: " + str(currFight["OPEN"]))

    @fightset.command(name="setup")
    async def fightset_setup(self):
        """Setup a new tournament!
        Default settings are as follows
        Name: Tourney # (counts from 0)
        Best of: 1
        Best of (final): 1
        Self Report: True
        Type: 0 (Round Robin)"""

        currServ = self.the_data[self.server.id]
        tourID = str(len(currServ["TOURNEYS"]))  # Can just be len without +1, tourney 0 makes len 1, tourney 1 makes len 2, etc
        currServ["CURRENT"] = tourID
        currServ["TOURNEYS"][tourID] = {"PLAYERS": [],
                                        "NAME": "Tourney "+str(tourID),
                                        "RULES": {"BESTOF": 1, "BESTOFFINAL": 1, "SELFREPORT": True, "TYPE": 0},
                                        "TYPEDATA": {},
                                        "OPEN": False,
                                        "WINNER": None}

        self.save_data()

        await self.bot.say("Tournament has been created!\n\n" + str(currServ["TOURNEYS"][tourID]))

        await self.bot.say("Adjust settings as necessary, then open the tournament with [p]fightset toggleopen")

    @fightset.command(name="stop", pass_context=True)
    async def fightset_stop(self, ctx):
        """Stops current tournament"""
        if not self._activefight():
            await self.bot.say("No active fight to adjust")
            return

        author = ctx.message.author
        currServ = self.the_data[self.server.id]

        await self.bot.say("Current fight ID is "+str(currServ["CURRENT"])+"\nOkay to stop? yes/no")

        answer = await self.bot.wait_for_message(timeout=120, author=author)

        if not answer.content.upper() in ["YES", "Y"]:
            await self.bot.say("Cancelled")
            return

        currServ["CURRENT"] = None

        self.save_data()
        await self.bot.say("Fight has been stopped")

# **********************Private command group start*********************
    def _activefight(self):
        """Checks if there is an active tournament already"""
        return self.the_data[self.server.id]["CURRENT"]

    async def _infight(self, user: discord.Member):
        """Checks if passed member is already in the tournament"""
        await self.bot.say("_infight Todo")

    async def _openregistration(self):
        """Checks if fight is accepting joins"""
        await self.bot.say("_openregistration Todo")

    async def _comparescores(self):
        """Checks user submitted scores for inconsistancies"""
        await self.bot.say("_comparescores Todo")

    async def _parsemember(self):
        await self.bot.say("Parsemember Todo")
        
    def _get_user_from_id(self, userid):
        return discord.utils.get(self.server.members, id=userid)
        
    def _get_server_from_id(self, serverid):
        return discord.utils.get(self.bot.servers, id=serverid)

    def _getcurrentFight(self, server):
        if not _activeFight(server):
            return None

        return self.the_data[server.id]["TOURNEYS"][self.the_data[server.id]["CURRENT"]]

# **********************Single Elimination***************************
    async def _elim_setup(self, tID):
        await self.bot.say("Elim setup todo")

    async def _elim_start(self, tID):
        await self.bot.say("Elim start todo")

    async def _elim_update(self, matchID, ):
        await self.bot.say("Elim update todo")


# **********************Round-Robin**********************************
    def _rr_setup(self, tID):

        theT = self.the_data["TOURNEYS"][tID]
        theD = theT["TYPEDATA"]
        
        get_schedule = self._rr_schedule(theT["PLAYERS"])
        
        theD = {"SCHEDULE": get_schedule[0], "MATCHES": get_schedule[1]}
        
        self.save_data()

    async def _rr_printround(self, tID, rID):

        theT = self.the_data["TOURNEYS"][tID]
        theD = theT["TYPEDATA"]

        await self.bot.say("Round "+str(rID))

        for match in theD["SCHEDULE"][rID]:
            await self.bot.say(theD["MATCHES"][match]["TEAM1"] + " vs " + theD["MATCHES"][match]["TEAM2"] + " || Match ID: " + match)

    async def _rr_start(self, tID):

        self._rr_setup(tID)

        await self.bot.say("**Tournament is Starting**")

        await self._rr_printround(tID)

    async def _rr_update(self, tID, t1points=0, t2points=0):
        
        theT = self.the_data["TOURNEYS"][tID]
        theD = theT["TYPEDATA"]
        
        if t1points != 0 or t2points != 0:
            theD["MATCHES"][tID]["TEAM1"] = t1points
            theD["MATCHES"][tID]["TEAM2"] = t2points
            self.save_data()
            return
        
        await self.bot.say("Entering scores for match ID: " + tID + "\n\n")
        await self.bot.say("How many points did " + theD["MATCHES"][tID]["TEAM1"] + " get?")
        answer = await self.bot.wait_for_message(timeout=120, author=author)
        try:
            t1points = int(answer.content)
        except:
            await self.bot.say("That's not a number!")
            return
            
        await self.bot.say("How many points did " + theD["MATCHES"][tID]["TEAM2"] + " get?")
        answer = await self.bot.wait_for_message(timeout=120, author=author)
        try:
            t2points = int(answer.content)
        except:
            await self.bot.say("That's not a number!")
            return
        
        if t1points == math.ceil(theD["RULES"]["BESTOF"]/2) or t2points == math.ceil(theD["RULES"]["BESTOF"]/2):
            theD["MATCHES"][tID]["TEAM1"] = t1points
            theD["MATCHES"][tID]["TEAM2"] = t2points
            self.save_data()
            return
        else:
            await self.bot.say("Invalid scores, nothing will be updated")
            return
        
    def _rr_schedule(inlist):
        """ Create a schedule for the teams in the list and return it"""
        s = []  # Schedule list
        outID = {}  # Matches
        
        firstID = ["A", "B", "C", "D", "E", "F",
                   "G", "H", "I", "J", "K", "L",
                   "M", "N", "O", "P", "Q", "R",
                   "S", "T", "U", "V", "W", "X",
                   "Y", "Z"]
                       
        if len(inlist) % 2 == 1:
            inlist = inlist + ["BYE"]

        for i in range(len(inlist)-1):

            mid = int(len(inlist) / 2)
            l1 = inlist[:mid]
            l2 = inlist[mid:]
            l2.reverse()

            matchLetter = ""
            j = i
            while j+1 > 26:

                matchLetter += firstID[int(j + 1) % 26 - 1]

                j = (j + 1) / 26 - 1
            matchLetter += firstID[int(j+1) % 26-1]
            matchLetter = matchLetter[::-1]

            matchID = []
            for ix in range(len(l1)-1):
                matchID += [matchLetter+str(ix)]

            rPlayers = list(zip(l1, l2))
            TeamCnt = 0
            for ID in matchID:
                outID[ID] = {"TEAM1": rPlayers[TeamCnt][0], "TEAM2": rPlayers[TeamCnt][1], "SCORE1": 0, "SCORE2": 0}
                TeamCnt += 1
                
            # List of match ID's is now done

            s += [matchID]  # Schedule of matches
            inlist.insert(1, inlist.pop())

        outlist = [[], {}]
        outlist[0] = s
        outlist[1] = outID
        # outlist[0] is list schedule of matches
        # outlist[1] is dict data of matches
        
        return outlist


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
