"""
This module handles the JSON configuration file.
"""

import logging
import sys
from utils.jsonfile import JsonFile

DEFAULT_CONFIG = {
    'token': 'token_here',
    'openai_key': 'openai_key_here',
    'command_prefix': '.',
    'status': 'wafflebunny | .help | v1.0b',
    'owner_id': 212056562452267008,
    'debug': False
}

class Config(JsonFile):

    """
    A class to handle configuration for the application, extending JSON file operations.

    :param str filepath: The path to the configuration file.
    """

    def __init__(self, filepath='config.json'):
        super().__init__(filepath)
        config_data = self.load()
        if config_data is None:
            logging.info('Auto-generating a new configuration file.')
            self.save(DEFAULT_CONFIG)
            logging.warning('Please modify the newly generated config and restart the application.')
            sys.exit()
        self.__dict__.update(config_data)
        logging.info('Successfully loaded the configuration file.')
