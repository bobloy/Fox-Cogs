import discord
import os

from discord.ext import commands
from random import randint, shuffle

from .utils.dataIO import dataIO
from .utils import checks

PRIME_LIST = [0, 1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
U_LETTERS = "🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


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
        self.leftcard = None
        self.rightcard = None
        self.answer = None
        self.answer_emoji = None


    async def pick_a_card(self, channel, user_scores):
        shuffle(self.cardlist)

        self.leftcard = self.cardlist.pop()
        self.rightcard = self.cardlist[-1]

        embed = self._card_embeds()
        
        await self.bot.send_message(channel, embed=embed)
        
        response = await self.bot.wait_for_message(timeout=20, channel=channel, content=self.answer)
        
        if not response:
            await self.bot.send_message(channel, "Timed-out! Answer was {}:{}\nEnding game".format(self.answer, str(self.answer_emoji)))
            self._stopgame()
        else:
            await self.bot.send_message(channel, "Correct! Answer was {}:{}".format(self.answer, str(self.answer_emoji)))

    def _card_embeds(self):
        embed=discord.Embed(title="Spot-It!", description="Identify the matching symbols!")
     
        card1 = list(self.leftcard)
        card2 = list(self.righcard)
        
        rev_u_letters = list(U_LETTERS[::-1])  # Reverse u_letters as a list
        rev_letters = list(LETTERS[::-1])  # Reverse letters as a list

        self.answer = self.check_cards(self.leftcard, self.rightcard)
        
        text1 = ""
        text2 = ""
        
        for x in range(len(card1)):
            if x%3 == 0:  # New line
                text1 += "\n"+rev_u_letters.pop()
                text2 += "\n⏹"
                rev_letters.pop()
            
            if sorted(self.leftcard)[x] == self.answer[0]:
                self.answer = rev_letters[-1]+"123"[x%3]
                self.answer_emoji = self.emojilist[card1[x]-1]
            
            text1 += str(self.emojilist[card1[x]-1])
            text2 += str(self.emojilist[card2[x]-1])
            
        text1 += "\n⏹:one::two::three:"
        text2 += "\n⏹⏹⏹⏹"
        

        embed.add_field(name="Card 1", value=text1, inline=True)
        embed.add_field(name="Card 2", value=text2, inline=True)
        
        return embed
        

    async def new_game(self):
        self.emojilist = await self.load_emojis()

        if not self.emojilist:
            print("Not enough custom emojis")
            return False

        for x in range(len(PRIME_LIST)):
            p = PRIME_LIST[x]
            if p * p + p + 1 > len(self.emojilist):
                self.cardlist, self.emojicount = self.create_cards(PRIME_LIST[x-1])
                return True

        print("How the hell do you have so many emojis available to you?")
        return False

    def create_cards(self, p):
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

    def check_cards(self, card1, card2):
        return sorted(card1 & card2)
              
    def save_data(self):
        """Saves the json"""
        dataIO.save_json(self.file_path, self.the_data)
    
    async def load_emojis(self):
        """Get all custom emojis from every server bot can see"""
        emoji_list = []
        for s in self.bot.servers:
            r = discord.http.Route('GET', '/guilds/{guild_id}', guild_id=s.id)
            j = await self.bot.http.request(r)
            g_emoji = [e for e in j['emojis']]
            emoji_list.extend(g_emoji)

        # for emoji in emoji_list:
            # await self.bot.say("{}".format(str(emoji)))
        
        return ["<{}:{}:{}>".format("a" if e['animated'] else "", e['name'], e['id']) for e in emoji_list]
        # return [r for server in self.bot.servers for r in server.emojis]
        
    @commands.group(aliases=['setspotit'], pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def spotitset(self, ctx):
        """Adjust Spot-It settings"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
            

    @commands.command(pass_context=True)
    async def spotit(self, ctx):
        """Start a new game of Spot-It"""
        if self.is_running:
            await self.bot.say("Game is already running\nStop it with `[p]endspotit`")
            return
        if not await self.new_game():
            await self.bot.say("Failed to start a new game, check console for more information")
            return
        
        user_scores = {}
        
        await self._startgame(ctx.message.channel, user_scores)
        
        if user_scores: # If anyone responded at all
            await self.bot.say("Here are the scores!")
            embed=discord.Embed(title="Spot-It Scores")
            for user in user_scores:
                embed.add_field(name=user.display_name, value="Points: {}".format(score), inline=False)
        
        
    @commands.command(aliases=['spotitend', 'stopspotit', 'spotitstop'], pass_context=True)
    async def endspotit(self, ctx):
        """Stops the current game of Spot-It!"""
        if not self.is_running:
            await self.bot.say("No game currently running")
            return
        self._stopgame()
        await self.bot.say("Game will be abandoned after timeout..")
    
    async def _startgame(self, channel, user_scores):
        """Starts a new game of Spot-It!"""
        self.is_running= True
        
        while self.is_running:  # Until someone stops it or times out or winner
            await self.pick_a_card(channel, user_scores)

        
    def _stopgame(self):
        """Stops the game in current state"""
        self.is_running = False



    
def check_folders():
    if not os.path.exists("data/Fox-Cogs"):
        print("Creating data/Fox-Cogs folder...")
        os.makedirs("data/Fox-Cogs")

    if not os.path.exists("data/Fox-Cogs/spotit"):
        print("Creating data/Fox-Cogs/spotit folder...")
        os.makedirs("data/Fox-Cogs/spotit")

        
def check_files():
    if not dataIO.is_valid_json("data/Fox-Cogs/spotit/spotit.json"):
        dataIO.save_json("data/Fox-Cogs/spotit/spotit.json", {})
    

def setup(bot):
    check_folders()
    check_files()
    n = Spotit(bot)
    bot.add_cog(n)
    
