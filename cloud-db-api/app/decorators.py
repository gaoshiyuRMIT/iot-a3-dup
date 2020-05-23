from flask import jsonify
from functools import wraps

def jsonifyResponseData(f):
    '''a decorator to wrap the return data of a view function in a json object with key "data"
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = f(*args, **kwargs)
        return jsonify({"data": data})
    return decorated_function