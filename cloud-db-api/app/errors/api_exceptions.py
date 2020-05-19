import json
from flask import jsonify

class BaseAPIException(Exception):
    status_code = 500
    error_code = "APIException"

    def __init__(self, message, status_code=None, error_code=None, payload=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if error_code is not None:
            self.error_code = error_code
        self.payload = payload

    def toDict(self):
        rv = {"error_code": self.error_code, "error_message": self.message}
        if self.payload is not None:
            rv["error_payload"] = dict(self.payload)
        return rv


class InvalidArgument(BaseAPIException):
    status_code = 400
    error_code = "InvalidArgument"

class MissingKey(BaseAPIException):
    status_code = 400
    error_code = "MissingKey"
        
class DuplicateKey(BaseAPIException):
    status_code = 400
    error_code = "DuplicateKey"
