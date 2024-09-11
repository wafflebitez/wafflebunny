import json
import logging
import os

"""
This module handles JSON file operations.
"""

class JsonFile:

    """
    A class to manage JSON file reading and writing.

    :param str filepath: The path of the JSON file to read/write to
    """

    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        """
        Loads the JSON file from the filepath 
        """
        if not os.path.exists(self.filepath):
            logging.error('"%s" not found!', self.filepath)
            return None
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            logging.error('Failed to decode JSON from "%s": %s', self.filepath, e)

    def save(self, data):
        """
        Saves the JSON file

        :param dict data: The data to be written in the JSON file
        """
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            logging.info('"%s" successfully saved.', self.filepath)
        except Exception as e:
            logging.error('Failed to save "%s": %s', self.filepath, e)
