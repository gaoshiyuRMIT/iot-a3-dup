from abc import ABC, abstractmethod
from flask import current_app
import requests as _r


class APIException(Exception):
    def __init__(self, error_code: str, error_message: str):
        self.error_code = error_code
        self.error_message = error_message


class BaseService(ABC):

    def __init__(self):
        self.BASE_URL = current_app.config["RESTFUL_API_ENDPOINT"]

    # POST data in json format
    # decode json response
    def post(self, url, data):
        resp = _r.post(self.BASE_URL + url, json=data)
        body = resp.json()
        if resp.status_code == _r.codes.ok:
            return body["data"]
        raise APIException(body["error_code"], body["error_message"])

    # GET with url params (?key1=value1&key=value2&...)
    # decode json response
    def get(self, url, params):
        resp = _r.get(self.BASE_URL + url, params=params)
        body = resp.json()
        if resp.status_code == _r.codes.ok:
            return body["data"]
        raise APIException(body["error_code"], body["error_message"])

    # PUT data in json format
    # decode json response
    def put(self, url, data):
        resp = _r.put(self.BASE_URL + url, json=data)
        body = resp.json()
        if resp.status_code == _r.codes.ok:
            return body["data"]
        raise APIException(body["error_code"], body["error_message"])
