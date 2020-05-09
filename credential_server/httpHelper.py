import requests as reqs
import json

class httpHelper:
    def __init__(self):
        self.address = 'http://127.0.0.1:5000'
        
    def post(self, user_detail):
        user_array = user_detail.split('/')
        data_set= {"username":user_array[0], "password":user_array[1]}
        print(data_set)
        # json_string = json.dumps(data_set)
        # json_object = json.loads(json_string)
        responses = reqs.post(self.address+'/users/login',json=data_set)

        try:
            if(json.loads(responses.text)['data']['success']):
                return True
        except:
            return False    
        
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