'''
Navsim module

'''

import json
from typing import Optional, Union, Dict, NewType, Any

ConfigValue = Union[str, int, bool]
ConfigStore = Dict[str, Union[ConfigValue, dict]]


class ConfigurationManager:
    ''' Used to load and store configuration values on inital load '''
    _db: ConfigStore = {}

    def __init__(self, file: Optional[str]):
        self.load(file)

    def load(self, file: Optional[str]):
        ''' Load a given filename, defaults to 'config.json' if blank '''
        try:
            self._db.update(json.load(open(file or 'config.json')))
        except json.JSONDecodeError:
            pass

    def get(self, key: str, default: ConfigValue) -> ConfigValue:
        '''Returns the loaded configuration value or default'''

        idx: Any = self._db

        for k in key.split('.'):
            idx = idx.get(k, default)

            if not isinstance(idx, dict):  # no deeper
                break

        return idx
