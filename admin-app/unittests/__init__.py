from unittest.mock import MagicMock, patch

RESTFUL_API_URL = "http://test.admin.app:6543"

def patch_current_app():
    mock_app = MagicMock()
    mock_app.config = {"RESTFUL_API_ENDPOINT": RESTFUL_API_URL}
    return patch("flask.current_app", mock_app)

from .services import *