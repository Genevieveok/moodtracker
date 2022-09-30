"""
Web app config details
database config details also set here
"""
DEBUG = False
SQLALCHEMY_ECHO = False

from dotenv import load_dotenv
from os import environ, path
import os


basedir = path.abspath(path.dirname(__file__))+'/moodtracker/'
load_dotenv(path.join(basedir, '.env'))
db_name = 'mood.db'


class Config:


    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI") or \
        'sqlite:///' + os.path.join(basedir, db_name)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
