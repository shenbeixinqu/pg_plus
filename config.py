import os
import logging

Base_dir = os.path.dirname(__file__)
# Base_url = "http://127.0.0.1:5000"
Base_url = "http://192.168.31.249:5000"
# Base_url = "http://waxh.pg024.com"


class Config(object):
    DEBUG = True
    DB_USERNAME = 'root'
    DB_PASSWORD = '123456'
    DB_HOST = '127.0.0.1'
    DB_PORT = '3306'
    DB_NAME = 'web_attack'
    DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopConfig(Config):
    LOGGING_LEVEL = logging.INFO


configs = {
    'default': Config,
    'develop': DevelopConfig
}
