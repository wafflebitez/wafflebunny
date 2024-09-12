"""
This module handles any classes/functions using selfcord.py.
"""

import logging
import openai
import os
import selfcord as discord
from selfcord.ext import commands

class wafflebunny(commands.Bot):

    def __init__(self, command_prefix: str, openai_key: str = None, owner_id: int = None, game: str = None):
        super().__init__(command_prefix = command_prefix, owner_id = owner_id)
        self.game = game
        if openai_key is not None:
            openai.api_key = openai_key
            self.openai = openai
        else:
            self.openai = None

    async def on_ready(self):
        """
        This function is called when selfcord successfully connects to the API.
        """
        for file in os.listdir('cogs'):
            if file.endswith('.py'):
                try:
                    await self.load_extension(f"cogs.{file[:-3]}")
                    logging.info('Loaded extension "%s"', file)
                except Exception as e:
                    logging.error('Error while loading extension "%s": %s', file, e)

        logging.info('Successfully connected as: %s', self.user)

        # update user status
        await self.change_presence(activity=discord.Game(name=self.game))

    async def on_message(self, msg):
        """
        This function is called whenever a message event is triggered.
        """
        await self.process_commands(msg)
