from flask import jsonify
from functools import wraps

def jsonifyResponseData(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = f(*args, **kwargs)
        return jsonify({"data": data})
    return decorated_function