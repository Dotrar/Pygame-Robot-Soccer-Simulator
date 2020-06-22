import logging
from io import StringIO

from . import ConfigurationManager

class Console:
    ''' Console object for storing messages '''
    _log_stream = StringIO()
    log = logging
    def __init__(self):
        self.log.basicConfig(stream= self._log_stream, )
        pass
