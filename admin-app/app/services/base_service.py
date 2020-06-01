from abc import ABC, abstractmethod
from flask import current_app
import requests as _r
from app.errors import APIException


class BaseService(ABC):

    def __init__(self):
        self.BASE_URL = current_app.config["RESTFUL_API_ENDPOINT"]

    def post(self, url, data):
        '''
        POST data in json format & decode json response

        :param str url: relative url of the API to call
        :param dict data: data to post 
        :return: response' json data
        :rtype: dict
        '''
        resp = _r.post(self.BASE_URL + url, json=data)
        body = resp.json()
        if resp.status_code == _r.codes.ok:
            return body["data"]
        raise APIException(body["error_code"], body["error_message"])

    def get(self, url, params = {}):
        '''
        GET with url params (?key1=value1&key=value2&...)
        decode json response

        :param str url: relative url of the API to call
        :param dict params: query params 
        :return: response' json data
        :rtype: dict
        '''
        resp = _r.get(self.BASE_URL + url, params=params)
        body = resp.json()
        if resp.status_code == _r.codes.ok:
            return body["data"]
        raise APIException(body["error_code"], body["error_message"])

    def put(self, url, data):
        '''
        PUT data in json format
        decode json response

        :param str url: relative url of the API to call
        :param dict params: data to put 
        :return: response' json data
        :rtype: dict
        '''
        resp = _r.put(self.BASE_URL + url, json=data)
        body = resp.json()
        if resp.status_code == _r.codes.ok:
            return body["data"]
        raise APIException(body["error_code"], body["error_message"])

    def delete(self, url):
        '''DELETE data
        '''
        resp = _r.delete(self.BASE_URL + url)
        body = resp.json()
        if resp.status_code == _r.codes.ok:
            return body["data"]
        raise APIException(body["error_code"], body["error_message"])
