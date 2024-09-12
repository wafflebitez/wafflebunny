"""
The main entry point for wafflebunny.
"""

import logging
import sys
import selfcord as discord
from utils.config import Config
from utils.bot import wafflebunny

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == '__main__':
    config = Config()
    bot = wafflebunny(command_prefix = config.command_prefix,
                      openai_key = config.openai_key,
                      owner_id = config.owner_id,
                      game = config.status
                      )
    try:
        bot.run(config.token)
    except discord.errors.LoginFailure as e:
        logging.error(e)
        sys.exit()
