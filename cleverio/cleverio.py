import discord

from discord.ext import commands

import requests
import json


class CleverBot(object):
    def __init__(self, user, key, nick=None):
        self.user = user
        self.key = key
        self.nick = nick

        body = {
            'user': user,
            'key': key,
            'nick': nick
        }

        requests.post('https://cleverbot.io/1.0/create', json=body)


    def query(self, text):
        body = {
            'user': self.user,
            'key': self.key,
            'nick': self.nick,
            'text': text
        }

        r = requests.post('https://cleverbot.io/1.0/ask', json=body)
        r = json.loads(r.text)

        if r['status'] == 'success':
            return r['response']
        else:
            return False


class Cleverio:
    """Cog for answering coding questions"""

    def __init__(self, bot):
        self.bot = bot
        self.name="JINruSYcSFZnT2qf"
        self.key="Ty2orHyWbSSnG9IOmLhV2dscyWvFclpF"
        self.clever = CleverBot(self.name, self.key)
        self.query = ""

    @commands.group(pass_context=True)
    async def cleverset(self, ctx):
        """Adjust cleverbot settings
        Settings are reset on reload"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
    
    @cleverset.command(pass_context=True, name="apikey")
    async def cleverset_apikey(self, ctx, name, key):
        """Adjust number of answers provided.
        Defaults to 1"""
        
        self.name = name
        self.key = key
        
        self.clever = CleverBot(self.name, self.key)
        await self.bot.say("New cleverbot acquired")
    
    @commands.command(pass_context=True)
    async def cleverio(self, ctx, *query):
        """Talk to cleverbot.io"""
        self.bot.type()
        self.query = " ".join(query)
        
        response = self.clever.query(self.query)
        
        if response:
            await self.bot.say(response)
        else:
            await self.bot.say(":thinking:")

    async def on_message(self, message):
        author = message.author
        channel = message.channel

        if message.author.id != self.bot.user.id:
            to_strip = "@" + author.server.me.display_name + " "
            text = message.clean_content
            if not text.startswith(to_strip):
                return
            text = text.replace(to_strip, "", 1)
            await self.bot.send_typing(channel)
            response = self.clever.query(self.query)
            if response:
                await self.bot.send_message(channel, response)
            else:
                await self.bot.send_message(channel, ":thinking:")
        
def setup(bot):
    n = Cleverio(bot)
    bot.add_cog(n)
