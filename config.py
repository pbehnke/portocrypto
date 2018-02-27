import os
from tempfile import mkdtemp

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SECRET_KEY = 'you-will-never-guess'
    # SESSION_FILE_DIR = mkdtemp()
    # SESSION_PERMANENT = False
    # SESSION_TYPE = "filesystem"
    

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RDS_DB_NAME = os.environ.get('RDS_DB_NAME')
    RDS_HOSTNAME = os.environ.get('RDS_HOSTNAME')
    RDS_PORT = os.environ.get('RDS_PORT')
    RDS_USERNAME = os.environ.get('RDS_USERNAME')
    RDS_PASSWORD = os.environ.get('RDS_PASSWORD')

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(RDS_USERNAME, RDS_PASSWORD, RDS_HOSTNAME, RDS_PORT, RDS_DB_NAME)

    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://matejmasteruser:Hh60600mmu@mydbinstance.cemwj7hglrfa.us-east-1.rds.amazonaws.com:3306/portoDB'
    # 'mysql+pymysql://flaskdemo:flaskdemo@flaskdemo.cwsaehb7ywmi.us-east-1.rds.amazonaws.com:3306/flaskdemo'
