import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # note: all-cap
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' 
    DEBUG = True
    # by default "http://localhost:6542", uncomment and fill in the below line to override. 
    # RESTFUL_API_ENDPOINT = ""