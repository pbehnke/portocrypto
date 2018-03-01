import os
from tempfile import mkdtemp

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RDS_DB_NAME = os.environ.get('RDS_DB_NAME')
    RDS_HOSTNAME = os.environ.get('RDS_HOSTNAME')
    RDS_PORT = os.environ.get('RDS_PORT')
    RDS_USERNAME = os.environ.get('RDS_USERNAME')
    RDS_PASSWORD = os.environ.get('RDS_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(RDS_USERNAME, RDS_PASSWORD, RDS_HOSTNAME, RDS_PORT, RDS_DB_NAME)
    MAIL_SERVER=os.environ.get('MAIL_SERVER')
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    MAIL_PORT=os.environ.get('MAIL_PORT')
    MAIL_USE_SSL=os.environ.get('MAIL_USE_SSL')
    MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS')
