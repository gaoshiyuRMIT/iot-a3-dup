from unittest.mock import MagicMock, patch
from unittests import patch_current_app

patcher_post = patch("requests.post")
patcher_get = patch("requests.get")
patcher_put = patch("requests.put")
patcher_app = patch_current_app()

mock_post = patcher_post.start()
mock_get = patcher_get.start()
mock_put = patcher_put.start()
mock_app = patcher_app.start()

from .test_base_services import TestBaseServices
from .test_booking_services import TestBookingServices
from .test_car_services import TestCarServices
from .test_user_services import TestUserServices

__all__ = [
    "TestBaseServices",
    'TestBookingServices',
    "TestCarServices",
    "TestUserServices"
]