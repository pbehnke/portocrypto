import os
from tempfile import mkdtemp

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # RDS_DB_NAME = os.environ.get('RDS_DB_NAME')
    # RDS_HOSTNAME = os.environ.get('RDS_HOSTNAME')
    # RDS_PORT = os.environ.get('RDS_PORT')
    # RDS_USERNAME = os.environ.get('RDS_USERNAME')
    # RDS_PASSWORD = os.environ.get('RDS_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(RDS_USERNAME, RDS_PASSWORD, RDS_HOSTNAME, RDS_PORT, RDS_DB_NAME)
