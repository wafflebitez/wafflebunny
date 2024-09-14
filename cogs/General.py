"""
This module serves general all-purpose commands
"""

import io
import json
import requests
import selfcord as discord
from selfcord.ext import commands
from fuzzywuzzy import process

class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.fetch_breeds()

    def fetch_breeds(self):
        """
        Queries the dog & cat APIs to populate dicts of valid breeds
        """
        self.cats, self.dogs = {}, {}

        r = requests.get("https://api.thecatapi.com/v1/breeds").json()
        for cat in r:
            self.cats[cat["id"]] = cat["name"]

        r = requests.get("https://api.thedogapi.com/v1/breeds").json()
        for dog in r:
            self.dogs[dog["id"]] = dog["name"]

    def fuzzy_match(self, query, data):
        """
        Fuzzy match the query against the provided data (dictionary keys and values).
        Returns the best match key if found, otherwise None.
        """
        match = process.extractOne(query, list(data.keys()) + list(data.values()))
        if match:
            return match[0] if match[0] in data else [key for key, value in data.items() if value == match[0]][0]
        return None
    
    def dict_to_json(self, data):
        """
        Converts a dictionary to a JSON file in memory.

        :param data dict: The dictionary to convert.
        
        Returns a BytesIO object containing the JSON file content.
        """
        json_data = json.dumps(data, indent=4)
        file = io.BytesIO(json_data.encode('utf-8'))
        return file

    @commands.command()
    async def ping(self, ctx):
        await ctx.reply(f"I'm still alive. `{round(self.bot.latency * 1000)}ms`")

    @commands.command()
    async def cat(self, ctx, *subcommand):
        if subcommand:
            # Join into a single string 
            subcommand = ' '.join(subcommand).lower()

            # List breeds if the 'breeds' subcommand is used
            if subcommand == 'breeds':
                file = self.dict_to_json(self.cats)
                return await ctx.send(file=discord.File(file, 'cat_breeds.json'))
            
            # Fuzzy match the breed or abbreviation
            breed_key = self.fuzzy_match(subcommand, self.cats)
            if breed_key:
                try:
                    data = requests.get(f'https://api.thecatapi.com/v1/images/search?breed_ids={breed_key}').json()
                except:
                    return await ctx.reply('An error occurred whilst fetching your cat image.')
            else:
                return await ctx.reply(f'Cat breed not found. Try using `{self.bot.command_prefix}cat breeds` for a list of breeds.')
            
        else:
            # No subcommand, fetch random cat image
            try:
                data = requests.get('https://api.thecatapi.com/v1/images/search').json()
            except:
                return await ctx.reply('An error occurred whilst fetching your cat image.')

        bot_response = data[0]['url']
        return await ctx.reply(bot_response)
    
    @commands.command()
    async def dog(self, ctx, *subcommand):
        if subcommand:
            # Join into single string
            subcommand = ' '.join(subcommand).lower()

            # List breeds if the 'breeds' subcommand is used
            if subcommand == 'breeds':
                file = self.dict_to_json(self.dogs)
                return await ctx.send(file=discord.File(file, 'dog_breeds.json'))

            # Fuzzy match the breed or abbreviation
            breed_key = self.fuzzy_match(subcommand, self.dogs)
            if breed_key:
                try:
                    data = requests.get(f'https://api.thedogapi.com/v1/images/search?breed_ids={breed_key}').json()
                except:
                    return await ctx.reply('An error occurred whilst fetching your dog image.')
            else:
                return await ctx.reply(f'Dog breed not found. Try using `{self.bot.command_prefix}dog breeds` for a list of breeds.')
            
        else:
            # No subcommand, fetch random dog image
            try:
                data = requests.get('https://api.thedogapi.com/v1/images/search').json()
            except:
                return await ctx.reply('An error occurred whilst fetching your dog image.')

        bot_response = data[0]['url']
        return await ctx.reply(bot_response)
    
    @commands.command(aliases=['rabbit'])
    async def bunny(self, ctx):
        try:
            data = requests.get('https://rabbit-api-two.vercel.app/api/random').json()
        except:
            return await ctx.reply('An error occured whilst fetching your bunny image.')
        return await ctx.reply(data['url'])

async def setup(bot):
    await bot.add_cog(General(bot))
