import requests as reqs
import json
from configparser import ConfigParser
config = ConfigParser()
config.read('ap.config', encoding='UTF-8')

class httpHelper:
    def __init__(self):
        self.address = 'http://127.0.0.1:6543'
        self.address = config['address'].get('apiAdd')
         
        
    def get(self, url):
        query = self.assemble_query(url)
        response = reqs.get(query)
        return response    
    
    def put(self,url,update):
        query = self.assemble_query(url)
        r = reqs.put(query, json=update)
        return r
    
    def post_data(self,url,data):
        query = self.assemble_query(url)
        response = reqs.post(query,json=data)
        return response
        
    
    def assemble_query(self,url):
        query = self.address + url
        return query
        
            

if __name__ == "__main__":
    helper = httpHelper()
    print(helper.post('a/b'))