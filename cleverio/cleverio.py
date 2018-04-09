from discord.ext import commands

import aiohttp
import os

from cogs.utils.dataIO import dataIO


class Cleverio:
    """Cog for answering coding questions"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
        self.apifile = "data/Cleverio/apikey.json"
        self.api = dataIO.load_json(self.apifile)
        self.clever = None

    def __unload(self):
        self.session.close()

    @commands.group(pass_context=True)
    async def cleverset(self, ctx):
        """Adjust cleverbot settings
        Settings are reset on reload"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @cleverset.command(pass_context=True, name="apikey")
    async def cleverset_apikey(self, ctx, user, key):
        """Adjust api key settings"""

        self.api["user"] = user
        self.api["key"] = key
        dataIO.save_json(self.apifile, self.api)
        nick = self.bot.user.name

        self.clever = await self.bot_instance(self.api["user"], self.api["key"], nick)
        await self.bot.say("New cleverbot acquired")

    @commands.command(pass_context=True)
    async def cleverio(self, ctx, *, query):
        """Talk to cleverbot.io"""
        self.bot.type()

        response = await self.bot_query(self.api["user"], self.api["key"], self.bot.user.name, query)

        if response:
            await self.bot.say(response)
        else:
            await self.bot.say(":thinking:")

    async def on_message(self, message):
        """
        Credit to https://github.com/Twentysix26/26-Cogs/blob/master/cleverbot/cleverbot.py
        for on_message recognition of @bot
        """
        author = message.author
        channel = message.channel
        if channel.is_private:  # author.server won't work
            return

        if message.author.id != self.bot.user.id:
            to_strip = "@" + author.server.me.display_name + " "
            text = message.clean_content
            if not text.startswith(to_strip):
                return
            text = text.replace(to_strip, "", 1)
            await self.bot.send_typing(channel)
            response = await self.bot_query(self.api["user"], self.api["key"], self.bot.user.name, text)
            if response:
                await self.bot.send_message(channel, response)
            else:
                await self.bot.send_message(channel, ":thinking:")

    async def bot_instance(self, user, key, nick):
        """Creates an bot instance"""
        data = {
            "user": user,
            "key": key,
            "nick": nick
        }
        async with self.session.post("https://cleverbot.io/1.0/create", data=data) as request:
            if request.status is not 200:
                return None
            return await request.json()

    async def bot_query(self, user, key, nick, query):
        """Querying cleverbot"""
        if self.clever is None:
            await self.bot_instance(user, key, nick)
        data = {
            "user": user,
            "key": key,
            "nick": nick,
            "text": query
        }
        async with self.session.post("https://cleverbot.io/1.0/ask", data=data) as request:
            if request.status is not 200:
                return None
            response = await request.json()
            return response["response"]  # Get JSON field "response" of HTTP-request response .-.


def check_folders():
    if not os.path.exists("data/Cleverio"):
        os.makedirs("data/Cleverio")


def check_files():
    system = {"user": "",
              "key": ""}
    f = "data/Cleverio/apikey.json"
    if not dataIO.is_valid_json(f):
        dataIO.save_json(f, system)


def setup(bot):
    check_folders()
    check_files()
    n = Cleverio(bot)
    bot.add_cog(n)
