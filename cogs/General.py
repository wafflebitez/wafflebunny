"""
This module serves general all-purpose commands
"""

import requests
import selfcord as discord
from selfcord.ext import commands

class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.reply(f"I'm still alive. `{round(self.bot.latency * 1000)}ms`")

    @commands.command()
    async def cat(self, ctx):
        try:
            data = requests.get('https://api.thecatapi.com/v1/images/search').json()
        except:
            return await ctx.reply('An error occured whilst fetching your cat image.')
        return await ctx.reply(data[0]['url'])

async def setup(bot):
    await bot.add_cog(General(bot))