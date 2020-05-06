from flask import jsonify, request
from app import app
from .api_exceptions import BaseAPIException

@app.errorhandler(500)
def internalServerErrorHandler(error):
    response = jsonify({"error_code": "InternalServerError", "error_message": "something went wrong internally"})
    response.status_code = 500
    return response

@app.errorhandler(404)
def notFoundErrorHandler(error):
    response = jsonify({"error_code": "NotFound", "error_message": "the page you are looking for does not exist"})
    response.status_code = 404
    return response

@app.errorhandler(405)
def methodNotAllowedHandler(error):
    response = jsonify({"error_code": "MethodNotAllowed", 
            "error_message": "the HTTP method {} is not allowed on this URL".format(request.method)})
    response.status_code = 405
    return response

@app.errorhandler(BaseAPIException)
def baseAPIExceptionHandler(error):
    response = jsonify(error.toDict())
    response.status_code = error.status_code
    return response
