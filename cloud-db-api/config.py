import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # note: all-cap
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' 
    DEBUG = True
    MYSQL_HOST = "1.2.3.4"
    MYSQL_USER = "root"
    MYSQL_DATABASE = "test"
    MYSQL_PASSWORD = "abcd1234"
