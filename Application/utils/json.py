"""
json.py
utilities for json stuff
"""
from flask.json import JSONEncoder as OldJSONEncoder

class JSONEncoder(OldJSONEncoder):

  def default(self, obj):
    try:
      return obj.__json__()
    except AttributeError:
      try:
        return obj.__serialize_pkey__()
      except AttributeError:
        pass
    return super().default(obj)
