import os
from tempfile import mkdtemp

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RDS_DB_NAME = 'portoDB'
    RDS_HOSTNAME = 'mydbinstance.cemwj7hglrfa.us-east-1.rds.amazonaws.com'
    RDS_PORT = '3306'
    RDS_USERNAME = 'matejmasteruser'
    RDS_PASSWORD = 'Hh60600mmu'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(RDS_USERNAME, RDS_PASSWORD, RDS_HOSTNAME, RDS_PORT, RDS_DB_NAME)
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://matejmasteruser:Hh60600mmu@mydbinstance.cemwj7hglrfa.us-east-1.rds.amazonaws.com:3306/portoDB'
