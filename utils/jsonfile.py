import json
import logging
import os

class JsonFile:
    def __init__(self, filepath):
        self.filepath = filepath
        
    def load(self):
        if not os.path.exists(self.filepath):
            logging.error(f'"{self.filepath}" not found!')
            return None
        try:
            with open(self.filepath, 'r') as file:
                return json.load(file)
        except Exception as e:
            logging.error(f'Failed to load {self.filepath}: {e}')
            return None

    def save(self, data):
        try:
            with open(self.filepath, 'w') as file:
                json.dump(data, file, indent=4)
            logging.info(f'"{self.filepath}" successfully saved.')
        except Exception as e:
            logging.error(f'Failed to save "{self.filepath}": {e}')
