import ipgetter
from discord.ext import commands

from cogs.utils import checks


class WhatsMyIP:
    """
    Assign roles based on trust rating
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def whatsmyip(self, ctx):
        """Print your bot's IP address"""
        my_ip = ipgetter.myip()

        await self.bot.send_message(ctx.message.author, "Your IP address is {}".format(my_ip))


def setup(bot):
    bot.add_cog(WhatsMyIP(bot))
