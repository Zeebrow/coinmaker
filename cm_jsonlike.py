import json
import logging
log = logging.getLogger(__name__)

class JsonLike(object):
    """Idea for a base class for Profile, Asset, and Order""" 
    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        _json = {}
        for k,v in self.__dict__:
            _json[k] = str(v)
        return _json
