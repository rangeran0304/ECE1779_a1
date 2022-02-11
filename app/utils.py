import base64
from flask import json

class Base64Encoder(json.JSONEncoder):
    # pylint: disable=method-hidden
    def default(self, o):
        if isinstance(o, bytes):
            return base64.b64encode(o).decode()
        return json.JSONEncoder.default(self, o)