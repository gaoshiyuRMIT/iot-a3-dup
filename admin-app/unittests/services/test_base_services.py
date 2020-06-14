import unittest as _ut
from unittest.mock import MagicMock, patch
from unittests import RESTFUL_API_URL
from . import mock_post, mock_get, mock_put, mock_app

class TestBaseServices(_ut.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_post = mock_post
        cls.mock_get = mock_get
        cls.mock_put = mock_put
        cls.mock_app = mock_app

    def tearDown(self):
        self.__class__.mock_post.reset_mock()
        self.__class__.mock_get.reset_mock()
        self.__class__.mock_put.reset_mock()
        self.__class__.mock_app.reset_mock()

    def test_post(self):
        '''confirm post method if passed the correct data & returns response data when status code is 200
        '''
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"data": "test post data"}
        self.mock_post.return_value = mock_resp
        from app.services.base_service import BaseService
        resp_data = BaseService().post("/test/base/services", {"field": "value"})
        self.mock_post.assert_called_with(f"{RESTFUL_API_URL}/test/base/services", json={"field": "value"})
        self.assertEqual("test post data", resp_data)

    def test_post_error_response(self):
        '''confirm post method raises api exception when status code is not 200
        '''
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        mock_resp.json.return_value = {"error_code": "InvalidArgument", "error_message": "invalid field `height` for a car"}
        self.mock_post.return_value = mock_resp
        from app.errors import APIException
        from app.services.base_service import BaseService
        with self.assertRaises(APIException):
            BaseService().post("/test/base/services", {"field": "value"})

    def test_get(self):
        '''confirm the `get` returns response data when status code is 200
        '''
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"data": "test get data"}
        self.mock_get.return_value = mock_resp
        from app.services.base_service import BaseService
        resp_data = BaseService().get("/test/base/services", {"field": "value"})
        self.mock_get.assert_called_with(f"{RESTFUL_API_URL}/test/base/services", params={"field": "value"})
        self.assertEqual("test get data", resp_data)

    def test_put(self):
        '''confirm that `put` returns response data when status code is 200
        '''
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"data": "test put data"}
        self.mock_put.return_value = mock_resp
        from app.services.base_service import BaseService
        resp_data = BaseService().put("/test/base/services", {"field": "value"})
        self.mock_put.assert_called_with(f"{RESTFUL_API_URL}/test/base/services", json={"field": "value"})
        self.assertEqual("test put data", resp_data)