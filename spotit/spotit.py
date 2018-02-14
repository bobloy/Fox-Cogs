import discord
import os

from discord.ext import commands
from random import randint

from .utils.dataIO import dataIO
from .utils import checks

PRIME_LIST = [0, 1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]

class Spotit:
    """Lets anyone play a game of hangman with custom phrases"""

    def __init__(self, bot):
        self.bot = bot
        self.path = "data/Fox-Cogs/spotit"
        self.file_path = "data/Fox-Cogs/spotit/spotit.json"
        self.the_data = dataIO.load_json(self.file_path)
        self.emojilist = []
        self.cardlist = [] 
        self.is_running = False
        self.emojicount = 0
    
    def new_game():
        self.emojilist = self.load_emojis()
        
        if not self.emojilist:
            print("Not enough custom emojis")
            return False
        
        for x in range(len(PRIME_LIST)):
            p = PRIME_LIST[x]
            if p * p + p + 1 > len(self.load_emojis()):
                self.cardslist, self.emojicount = self.create_cards(PRIME_LIST[x-1])
                return True
        
        print("How the hell do you have so many emojis available to you?")
        return False

    def create_cards(p):
        for min_factor in range(2, 1 + int(p ** 0.5)):
            if p % min_factor == 0:
                break
        else:
            min_factor = p
        cards = []
        for i in range(p):
            cards.append(set([i * p + j for j in range(p)] + [p * p]))
        for i in range(min_factor):
            for j in range(p):
                cards.append(set([k * p + (j + i * k) % p
                                  for k in range(p)] + [p * p + 1 + i]))

        cards.append(set([p * p + i for i in range(min_factor + 1)]))
        return cards, p * p + p + 1

    def check_cards(card1, card2):
        return sorted(card & other_card)
              
    def save_data(self):
        """Saves the json"""
        dataIO.save_json(self.file_path, self.the_data)
    
    def load_emojis(self):
        """Get all custom emojis from every server bot can see"""
        return [r for server in self.bot.servers for r in server.emojis]
        
    @commands.group(aliases=['setspotit'], pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def spotitset(self, ctx):
        """Adjust Spot-It settings"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
            
    @spotitset.command(pass_context=True)
    async def servers(self, ctx):
        message = ctx.message
        #Borrowing FlapJack's emoji validation (https://github.com/flapjax/FlapJack-Cogs/blob/master/smartreact/smartreact.py)
        if theface[:2] == "<:":
            theface = [r for server in self.bot.servers for r in server.emojis if r.id == theface.split(':')[2][:-1]][0]
        
        try:
            # Use the face as reaction to see if it's valid (THANKS FLAPJACK <3)
            await self.bot.add_reaction(message, theface)

        except discord.errors.HTTPException:
            await self.bot.say("That's not an emoji I recognize.")
        else:
            self.the_data["theface"] = str(theface)
            self.save_data()
            self._updateHanglist()
            await self.bot.say("Face has been updated!")
            
    @commands.command(pass_context=True)
    async def spotit(self, ctx):
        """Start a new game of Spot-It"""
        if not self.newgame():
            await self.bot.say("Failed to start a new game, check console for more information")
            return
        
        user_scores = {}
        
        await self.pick_a_card(ctx, user_scores)
        
        if user_scores: # If anyone responded at all
            await self.bot.say("Here are the scores!")
            embed=discord.Embed(title="Spot-It Scores")
            for user in user_scores:
                embed.add_field(name=user.display_name, value="Points: {}".format(score), inline=False)
        
        
    @commands.command(aliases=['spotitend', 'stopspotit', 'spotitstop'], pass_context=True)
    async def endspotit(self, ctx):
        """Stops the current game of hangman"""
        if not self.is_running:
            await self.bot.say("No game currently running")
            return
        self._stopgame()
        await self.bot.say("Game has been abandoned..")
    
    def _startgame(self):
        """Starts a new game of hangman"""
        self.the_data["answer"] = self._getphrase().upper()
        self.the_data["hangman"] = 0
        self.the_data["guesses"] = []
        self.winbool = False
        self.the_data["running"] = True
        self.the_data["trackmessage"] = False
        self.save_data()
        
    def _stopgame(self):
        """Stops the game in current state"""
        self.the_data["running"] = False
        self.save_data()
    
    async def _checkdone(self, channel=None):
        if self.winbool:
            if channel:
                await self.bot.send_message(channel, "You Win!")
            else:
                await self.bot.say("You Win!")
            self._stopgame()
                
        if self.the_data["hangman"] >= 7:
            if channel:
                await self.bot.send_message(channel, "You Lose!\nThe Answer was: **"+self.the_data["answer"]+"**")
            else:
                await self.bot.say("You Lose!\nThe Answer was: **"+self.the_data["answer"]+"**")
                
            self._stopgame()
                
    def _getphrase(self):
        """Get a new phrase for the game and returns it"""
        phrasefile = open(self.answer_path, 'r')
        phrases = phrasefile.readlines()
        
        outphrase = ""
        while outphrase == "":
            outphrase = phrases[randint(0, len(phrases)-1)].partition(" (")[0]
#           outphrase = phrases[randint(0,10)].partition(" (")[0]
        return outphrase
   
    def _hideanswer(self):
        """Returns the obscured answer"""
        out_str = ""
        
        self.winbool = True
        for i in self.the_data["answer"]:
            if i == " " or i == "-":
                out_str += i*2
            elif i in self.the_data["guesses"] or i not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                out_str += "__"+i+"__ "
            else:
                out_str += "**\_** "
                self.winbool = False
                
        return out_str
        
    def _guesslist(self):
        """Returns the current letter list"""
        out_str = ""
        for i in self.the_data["guesses"]:
            out_str += str(i) + ","
        out_str = out_str[:-1]
        
        return out_str
        
    async def _guessletter(self, guess, channel=None):
        """Checks the guess on a letter and prints game if acceptable guess"""
        if not guess.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or not len(guess) == 1:
            if channel:
                await self.bot.send_message(channel, "Invalid guess. Only A-Z is accepted")
            else:
                await self.bot.say("Invalid guess. Only A-Z is accepted")
            return

        if guess.upper() in self.the_data["guesses"]:
            if channel:
                await self.bot.send_message(channel, "Already guessed that! Try again")
            else:
                await self.bot.say("Already guessed that! Try again")
            return

        if not guess.upper() in self.the_data["answer"]:
            self.the_data["hangman"] += 1
            
        self.the_data["guesses"].append(guess.upper())
        self.save_data()
        
        await self._printgame(channel)
        
    async def _on_react(self, reaction, user):
        """ Thanks to flapjack reactpoll for guidelines
            https://github.com/flapjax/FlapJack-Cogs/blob/master/reactpoll/reactpoll.py"""
        
        
        
        if not self.the_data["trackmessage"]:
            return
        
        if user == self.bot.user:
            return  # Don't remove bot's own reactions
        message = reaction.message
        emoji = reaction.emoji
        
        if not message.id == self.the_data["trackmessage"]:
            return
        
        if str(emoji) in self.letters:
            letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[self.letters.index(str(emoji))]
            await self._guessletter(letter, message.channel)
            
            
        if str(emoji) in self.navigate:
            if str(emoji) == self.navigate[0]:
                await self._reactmessage_am(message)
            
            if str(emoji) == self.navigate[-1]:
                await self._reactmessage_nz(message)
    
    
    async def _reactmessage_menu(self, message):
        """React with menu options"""
        await self.bot.clear_reactions(message)
        
        await self.bot.add_reaction(message, self.navigate[0])
        await self.bot.add_reaction(message, self.navigate[-1])
        
    async def _reactmessage_am(self, message):
        await self.bot.clear_reactions(message)

        for x in range(len(self.letters)):
            if x in [i for i,b in enumerate("ABCDEFGHIJKLM") if b not in self._guesslist()]:
                await self.bot.add_reaction(message, self.letters[x])
         
        await self.bot.add_reaction(message, self.navigate[-1])


    async def _reactmessage_nz(self, message):
        await self.bot.clear_reactions(message)

        for x in range(len(self.letters)):
            if x in [i for i,b in enumerate("NOPQRSTUVWXYZ") if b not in self._guesslist()]:
                await self.bot.add_reaction(message, self.letters[x+13])
                
        await self.bot.add_reaction(message, self.navigate[0])        


    async def _printgame(self, channel=None):
        """Print the current state of game"""
        cSay = ("Guess this: " + str(self._hideanswer()) + "\n"
                + "Used Letters: " + str(self._guesslist()) + "\n"
                + self.hanglist[self.the_data["hangman"]] + "\n"
                + self.navigate[0]+" for A-M, "+self.navigate[-1]+" for N-Z")
        if channel:
            message = await self.bot.send_message(channel, cSay)
        else:
            message = await self.bot.say(cSay)
        
        self.the_data["trackmessage"] = message.id
        self.save_data()
        await self._reactmessage_menu(message)
        await self._checkdone(channel)
        
    
def check_folders():
    if not os.path.exists("data/Fox-Cogs"):
        print("Creating data/Fox-Cogs folder...")
        os.makedirs("data/Fox-Cogs")

    if not os.path.exists("data/Fox-Cogs/hangman"):
        print("Creating data/Fox-Cogs/hangman folder...")
        os.makedirs("data/Fox-Cogs/hangman")

        
def check_files():
    if not dataIO.is_valid_json("data/Fox-Cogs/hangman/hangman.json"):
        dataIO.save_json("data/Fox-Cogs/hangman/hangman.json", {"running": False, "hangman": 0, "guesses": [], "theface": "<:never:336861463446814720>", "trackmessage": False})
    

def setup(bot):
    check_folders()
    check_files()
    n = Hangman(bot)
    bot.add_cog(n)
    bot.add_listener(n._on_react, "on_reaction_add")
    
