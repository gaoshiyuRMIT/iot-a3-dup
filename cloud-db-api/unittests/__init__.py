from unittest.mock import MagicMock, patch

def patch_flask_request(json_data = {}):
    mock_req = MagicMock()
    mock_req.json = json_data
    return patch("flask.request", mock_req)

def patch_jsonify():
    return patch("flask.jsonify", MagicMock())



from .db import *
from .routes import *