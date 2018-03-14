import discord

from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks
from .utils.chat_formatting import pagify, box
import os
import re


class CCRole:
    """Custom commands
    Creates commands used to display text"""

    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/ccrole/commands.json"
        self.c_commands = dataIO.load_json(self.file_path)

    @commands.group(pass_context=True, no_pm=True)
    async def ccrole(self, ctx):
        """Custom commands management"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @ccrole.command(name="add", pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def ccrole_add(self, ctx, command : str):
        """Adds a custom command with roles"""
        command = command.lower()
        if command in self.bot.commands:
            await self.bot.say("That command is already a standard command.")
            return

        server = ctx.message.server
        author = ctx.message.author
        
        # Roles to add
        await self.bot.say('What roles should it add? (Must be comma separated)\nSay `None` to skip adding roles')
        
        answer = await self.bot.wait_for_message(timeout=120, author=author)
        if not answer:
            await self.bot.say("Timed out, canceling")
            return
        if answer.content.upper()!="NONE":
            role_list = answer.content.split(",")
            
            try:
                role_list = [discord.utils.get(server.roles, role) for role in role_list]
            except:
                await self.bot.say("Invalid answer, canceling")
                return
        
        

        
        if server.id not in self.c_commands:
            self.c_commands[server.id] = {}
        cmdlist = self.c_commands[server.id]
        if command not in cmdlist:
            cmdlist[command] = text
            self.c_commands[server.id] = cmdlist
            dataIO.save_json(self.file_path, self.c_commands)
            await self.bot.say("Custom command successfully added.")
        else:
            await self.bot.say("This command already exists. Delete"
                               "`it with {}ccrole delete` first."
                               "".format(ctx.prefix))

    @customcom.command(name="delete", pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def ccrole_delete(self, ctx, command : str):
        """Deletes a custom command
        Example:
        [p]customcom delete yourcommand"""
        server = ctx.message.server
        command = command.lower()
        if server.id in self.c_commands:
            cmdlist = self.c_commands[server.id]
            if command in cmdlist:
                cmdlist.pop(command, None)
                self.c_commands[server.id] = cmdlist
                dataIO.save_json(self.file_path, self.c_commands)
                await self.bot.say("Custom command successfully deleted.")
            else:
                await self.bot.say("That command doesn't exist.")
        else:
            await self.bot.say("There are no custom commands in this server."
                               " Use `{}customcom add` to start adding some."
                               "".format(ctx.prefix))

    @customcom.command(name="list", pass_context=True)
    async def ccrole_list(self, ctx):
        """Shows custom commands list"""
        server = ctx.message.server
        commands = self.c_commands.get(server.id, {})

        if not commands:
            await self.bot.say("There are no custom commands in this server."
                               " Use `{}customcom add` to start adding some."
                               "".format(ctx.prefix))
            return

        commands = ", ".join([ctx.prefix + c for c in sorted(commands)])
        commands = "Custom commands:\n\n" + commands

        if len(commands) < 1500:
            await self.bot.say(box(commands))
        else:
            for page in pagify(commands, delims=[" ", "\n"]):
                await self.bot.whisper(box(page))

    async def on_message(self, message):
        if len(message.content) < 2 or message.channel.is_private:
            return

        server = message.server
        prefix = self.get_prefix(message)

        if not prefix:
            return

        if server.id in self.c_commands and self.bot.user_allowed(message):
            cmdlist = self.c_commands[server.id]
            cmd = message.content[len(prefix):]
            if cmd in cmdlist:
                cmd = cmdlist[cmd]
                cmd = self.format_cc(cmd, message)
                await self.bot.send_message(message.channel, cmd)
            elif cmd.lower() in cmdlist:
                cmd = cmdlist[cmd.lower()]
                cmd = self.format_cc(cmd, message)
                await self.bot.send_message(message.channel, cmd)

    def get_prefix(self, message):
        for p in self.bot.settings.get_prefixes(message.server):
            if message.content.startswith(p):
                return p
        return False

    def format_cc(self, command, message):
        results = re.findall("\{([^}]+)\}", command)
        for result in results:
            param = self.transform_parameter(result, message)
            command = command.replace("{" + result + "}", param)
        return command

    def transform_parameter(self, result, message):
        """
        For security reasons only specific objects are allowed
        Internals are ignored
        """
        raw_result = "{" + result + "}"
        objects = {
            "message" : message,
            "author"  : message.author,
            "channel" : message.channel,
            "server"  : message.server
        }
        if result in objects:
            return str(objects[result])
        try:
            first, second = result.split(".")
        except ValueError:
            return raw_result
        if first in objects and not second.startswith("_"):
            first = objects[first]
        else:
            return raw_result
        return str(getattr(first, second, raw_result))


def check_folders():
    if not os.path.exists("data/customcom"):
        print("Creating data/customcom folder...")
        os.makedirs("data/customcom")


def check_files():
    f = "data/customcom/commands.json"
    if not dataIO.is_valid_json(f):
        print("Creating empty commands.json...")
        dataIO.save_json(f, {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(CCRole(bot))