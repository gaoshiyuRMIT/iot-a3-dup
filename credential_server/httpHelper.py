import requests as reqs
import json
from configparser import ConfigParser
config = ConfigParser()
config.read('server.config', encoding='UTF-8')

class httpHelper:
    """
    this class can send and recieve data from the api
    """
    def __init__(self):
        self.address = config['address'].get('apiAdd')
         
        
    def get(self, url):
        """http get

        :param string data: a partial url

        :return: response from the api
        :rtype: response"""
        query = self.assemble_query(url)
        response = reqs.get(query)
        return response    
    
    def put(self,url,update):
        """http put

        :param string data: a partial url
        :param json update: the put data

        :return: response from the api
        :rtype: response"""
        query = self.assemble_query(url)
        r = reqs.put(query, json=update)
        return r
    
    def post_data(self,url,data):
        """http post
        :param string data: a partial url
        :param json update: the post data

        :return: response from the api
        :rtype: response"""
        query = self.assemble_query(url)
        response = reqs.post(query,json=data)
        return response
        
    
    def assemble_query(self,url):
        """assemble the query"""
        query = self.address + url
        return query
        
            

if __name__ == "__main__":
    helper = httpHelper()
    print(helper.post('a/b'))