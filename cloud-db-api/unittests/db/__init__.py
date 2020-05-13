import pymysql

from unittest.mock import MagicMock, patch
from unittests.test_config import test_config as cfg


def patch_flask_g():
    mock_g = MagicMock()
    mock_g.__contains__.return_value = True
    mock_g.conn = pymysql.connect(cfg["MYSQL_HOST"], cfg["MYSQL_USER"], cfg["MYSQL_PASSWORD"], cfg["MYSQL_DATABASE"])
    return patch("flask.g", mock_g)

from .test_car_manager import TestCarManager