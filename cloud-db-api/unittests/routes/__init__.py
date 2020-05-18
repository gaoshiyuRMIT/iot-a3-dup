from unittest.mock import MagicMock, patch
from unittests import patch_flask_request


patcher_jsonify = patch("flask.jsonify")
patcher_req = patch_flask_request()
mock_jsonify = patcher_jsonify.start()
mock_req = patcher_req.start()


from .bookings import TestBookingsRoute
from .cars import TestCarsRoute
from .users import TestUsersRoute


__all__ = [
    "TestBookingsRoute",
    "TestCarsRoute",
    "TestUsersRoute"
]